# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from fastapi import HTTPException, status, Depends, Cookie
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, AuthSession
from .async_session import get_async_session
from .auth_session import get_current_auth_session_optional


__all__ = ['get_current_user_optional', 'get_current_user']


async def get_current_user_optional(
        session: AsyncSession = Depends(get_async_session),
        auth_session: t.Optional[AuthSession] = Depends(get_current_auth_session_optional),
) -> t.Optional[User]:
    if auth_session is None:
        return None

    stmt = sql.select(User).where(User.id == auth_session.user_id)
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
