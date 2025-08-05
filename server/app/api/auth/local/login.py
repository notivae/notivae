# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends, Body, Request, Response
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.core.dependencies import get_async_session, get_current_user_optional, rate_limited
from app.db.models import User, AuthIdentity, AuthSession, MFACredentials
from app.core.security.local import verify_password
from app.core.security.auth_session import generate_session_token, hash_session_token
from app.core.util import get_client_ip
from ._common import AuthLocalIdentityContext


router = APIRouter()


class LoginRequest(BaseModel):
    username_or_email: str = Field(...)
    password: str = Field(...)


class LoginResponse(BaseModel):
    success: bool
    requires_mfa: bool


@router.post(
    path='/login',
    response_model=LoginResponse,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=5/60))],
)
async def auth_local_login(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user_optional),
        form_data: LoginRequest = Body(),
) -> LoginResponse:
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already logged in",
        )

    stmt = sql.select(AuthIdentity) \
        .where(AuthIdentity.provider == 'local',
               sql.or_(AuthIdentity.provider_user_id == form_data.username_or_email,
                       AuthIdentity.provider_email == form_data.username_or_email))
    identity: AuthIdentity = await session.scalar(stmt)

    if identity is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    context = AuthLocalIdentityContext.model_validate(identity.context)

    if not verify_password(plain_password=form_data.password, hashed_password=context.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == identity.user_id, MFACredentials.confirmed.is_(True))
    mfa_credentials: MFACredentials = await session.scalar(stmt)  # one is enough

    session_token = generate_session_token()

    auth_session = AuthSession(
        user_id=identity.user_id,
        hashed_token=hash_session_token(session_token=session_token),
        user_agent=request.headers.get("User-Agent"),
        ip_address=get_client_ip(request=request),
        is_mfa_authenticated=False if mfa_credentials else None,
    )
    session.add(auth_session)
    await session.commit()

    response.set_cookie(
        key="session_token",
        value=session_token,
        expires=auth_session.expires_at,
        path="/api",
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return LoginResponse(
        success=True,
        requires_mfa=auth_session.is_mfa_authenticated is False,
    )
