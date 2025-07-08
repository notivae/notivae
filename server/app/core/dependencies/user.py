# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from fastapi import HTTPException, status, Depends, Cookie
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Session
from ..security.session import hash_session_token
from .session import get_async_session


__all__ = ['get_current_user_optional', 'get_current_user']


async def get_current_user_optional(
        session: AsyncSession = Depends(get_async_session),
        session_token: t.Optional[str] = Cookie(default=None),
) -> t.Optional[User]:
    if session_token is None:
        return None

    session_token_hashed = hash_session_token(session_token)

    stmt = sql.select(Session).where(Session.hashed_token == session_token_hashed)
    access_session: Session = await session.scalar(stmt)
    if access_session is None or access_session.revoked or access_session.expires_at < dt.datetime.now(dt.UTC):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired or revoked session token",
        )

    stmt = sql.select(User).where(User.id == access_session.user_id)
    user: User = await session.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not approved",
        )

    return user


async def get_current_user(
        user: t.Optional[User] = Depends(get_current_user_optional),
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing authentication",
        )
    return user
