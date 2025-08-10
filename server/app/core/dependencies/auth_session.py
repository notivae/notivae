# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from fastapi import HTTPException, status, Depends, Cookie
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuthSession
from app.core.security.auth_session import hash_session_token
from .async_session import get_async_session


__all__ = ['get_current_auth_session_optional', 'get_current_auth_session']


async def get_current_auth_session_optional(
        session: AsyncSession = Depends(get_async_session),
        session_token: t.Optional[str] = Cookie(default=None),
) -> t.Optional[AuthSession]:
    if session_token is None:
        return None

    session_token_hashed = hash_session_token(session_token)

    stmt = sql.select(AuthSession).where(AuthSession.hashed_token == session_token_hashed)
    auth_session: AuthSession = await session.scalar(stmt)
    if not AuthSession.is_valid(auth_session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired or revoked session token",
        )

    return auth_session


async def get_current_auth_session(
        auth_session: t.Optional[AuthSession] = Depends(get_current_auth_session_optional),
) -> AuthSession:
    if auth_session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing session token",
        )
    return auth_session
