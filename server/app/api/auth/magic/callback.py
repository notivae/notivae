# -*- coding=utf-8 -*-
r"""

"""
import time
import structlog
from fastapi import APIRouter, HTTPException, status, Request, Query, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from jose import JWTError, ExpiredSignatureError
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.util import get_client_ip
from app.core.dependencies import get_async_session, get_current_user_optional, rate_limited
from app.db.models import User, AuthSession, MFACredentials
from app.core.security.magic_link import parse_magic_link_token
from app.core.security.auth_session import generate_session_token, hash_session_token
from app.core.redis import redis_client


router = APIRouter()
logger = structlog.get_logger()


@router.get(
    path='/callback',
    response_class=RedirectResponse,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=5/300))],
)
async def magic_callback(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        logged_in_user: User = Depends(get_current_user_optional),
        token: str = Query(),
):
    try:
        claims = parse_magic_link_token(token=token)
    except ExpiredSignatureError:
        logger.warning("Expired token received")
        raise HTTPException(  # todo: proper redirect to login page
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The token has expired",
        )
    except (JWTError, ValidationError) as e:
        logger.error(f"invalid-token ({type(e)}: {e})", exc_info=e, token=token)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token received",
        )

    if logged_in_user is not None and str(logged_in_user.id) == claims.sub:
        return RedirectResponse(url="/")

    cache_key = f"magic-link:{claims.jti}"
    cached = await redis_client.get(cache_key)
    if cached:
        logger.error("Used magic-link token found. Probable replay attack detected")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    ttl = int(claims.exp.timestamp() - time.time())
    await redis_client.set(cache_key, 1, ex=ttl)

    stmt = sql.select(User).where(User.id == claims.sub)
    user: User = await session.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == user.id, MFACredentials.confirmed.is_(True))
    mfa_credentials: MFACredentials = await session.scalar(stmt)  # one is enough

    session_token = generate_session_token()

    auth_session = AuthSession(
        user_id=user.id,
        hashed_token=hash_session_token(session_token=session_token),
        user_agent=request.headers.get("User-Agent"),
        ip_address=get_client_ip(request=request),
        is_mfa_authenticated=False if mfa_credentials else None,
    )
    session.add(auth_session)
    await session.commit()

    response = RedirectResponse(url="/")
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
