# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import httpx
import structlog
from fastapi import APIRouter, HTTPException, status, Request, Query, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import SETTINGS, AccountCreationMode
from app.core.dependencies import get_current_user_optional, get_async_session, rate_limited
from app.core.security.auth_session import generate_session_token, hash_session_token
from app.core.security import oidc
from app.core.util import get_client_ip
from app.core.structures.oidc import OpenIdToken, OpenIdUserInfo
from app.db.models import User, AuthSession, AuthIdentity, MFACredentials
from app.core.reusables.verification_mail import send_verification_email
from app.core.reusables.account_approval import send_admin_account_approval_email
from ._common import decode_state


router = APIRouter()
logger = structlog.get_logger()


class OidcClaims(t.TypedDict):
    iss: str
    sub: str
    aud: str
    exp: int
    nonce: str

    email: str
    email_verified: t.NotRequired[bool]
    name: str
    preferred_username: str


@router.get(
    path='/callback',
    response_class=RedirectResponse,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def oidc_callback(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        user: t.Optional[User] = Depends(get_current_user_optional),
        code: str = Query(),
        state: str = Query(),
):
    try:
        state = decode_state(state)
    except Exception:
        logger.warning("Invalid state received")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state",
        )

    oidc_configuration = await oidc.get_configuration(discovery_uri=SETTINGS.OIDC.DISCOVERY_URI)

    redirect_uri = str(request.base_url).rstrip("/") + request.url.path

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=str(oidc_configuration.token_endpoint),
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
            },
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            auth=(SETTINGS.OIDC.CLIENT_ID, SETTINGS.OIDC.CLIENT_SECRET),
        )
        if not response.is_success:
            logger.error("failed to exchange code for token", response=response.text)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Could not exchange code for token",
            )
        token = OpenIdToken.model_validate_json(response.content)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=str(oidc_configuration.userinfo_endpoint),
            headers={
                'Accept': 'application/json',
                'Authorization': f"{token.token_type} {token.access_token}",
            },
        )
        if not response.is_success:
            logger.error("failed to obtain user information", response=response.text)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Could not obtain user information",
            )
        userinfo = OpenIdUserInfo.model_validate_json(response.content)

    stmt = sql.select(AuthIdentity) \
        .where(AuthIdentity.provider == "oidc", AuthIdentity.provider_user_id == userinfo.sub)
    auth_identity: AuthIdentity = await session.scalar(stmt)

    if auth_identity:
        if user and user.id != auth_identity.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Logged in user doesn't match with identity user",
            )

        # -- ensure up-to-date information --
        auth_identity.provider_email = userinfo.email
        auth_identity.userinfo = userinfo.model_dump(mode='json')
        if session.is_modified(auth_identity):
            await session.commit()
    else:
        # -- account creation --
        if user is None:
            if SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.CLOSED:
                raise HTTPException(  # todo: json response is not good in redirect-flow
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account creation is currently closed",
                )

            user = User(
                email=userinfo.email,
                name=userinfo.preferred_username,
                display_name=userinfo.name,
                is_approved=SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.OPEN,
            )
            session.add(user)
            await session.flush()

            background_tasks.add_task(send_verification_email, request=request, user=user)
            if SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.RESTRICTED:
                background_tasks.add_task(send_admin_account_approval_email, request=request, user=user)

        # -- identity linking --
        auth_identity = AuthIdentity(
            user_id=user.id,
            provider="oidc",
            provider_user_id=userinfo.sub,
            provider_email=userinfo.email,
            userinfo=userinfo.model_dump(mode='json'),
        )
        session.add(auth_identity)
        await session.commit()

    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == auth_identity.user_id, MFACredentials.confirmed.is_(True))
    mfa_credentials: MFACredentials = await session.scalar(stmt)  # one is enough

    session_token = generate_session_token()

    auth_session = AuthSession(
        user_id=auth_identity.user_id,
        hashed_token=hash_session_token(session_token=session_token),
        user_agent=request.headers.get("User-Agent"),
        ip_address=get_client_ip(request=request),
        is_mfa_authenticated=False if mfa_credentials else None,
    )
    session.add(auth_session)
    await session.commit()

    response = RedirectResponse(url=state.next_url)

    response.set_cookie(
        key="session_token",
        value=session_token,
        expires=auth_session.expires_at,
        path="/api",
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return response
