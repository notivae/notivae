# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from fastapi import HTTPException, status, Depends, Cookie
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuthSession
from app.core.security.auth_session import hash_session_token
from .async_session import get_async_session


async def get_current_auth_session_optional(
        session: AsyncSession = Depends(get_async_session),
        session_token: t.Optional[str] = Cookie(default=None),
) -> t.Optional[AuthSession]:
    if session_token is None:
        return None

    session_token_hashed = hash_session_token(session_token)

    stmt = sql.select(AuthSession).where(AuthSession.hashed_token == session_token_hashed)
    auth_session: AuthSession = await session.scalar(stmt)
    if auth_session is None or auth_session.revoked or auth_session.expires_at < dt.datetime.now(dt.UTC):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired or revoked session token",
        )

    return auth_session
