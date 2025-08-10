# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Response, status, Depends, Cookie
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import rate_limited, get_async_session
from app.core.security.auth_session import hash_session_token
from app.db.models import AuthSession


router = APIRouter()


@router.post(
    path='/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def logout(
        response: Response,
        session: AsyncSession = Depends(get_async_session),
        session_token: str | None = Cookie(default=None),
) -> None:
    session_token_hashed = hash_session_token(session_token)

    stmt = sql.select(AuthSession).where(AuthSession.hashed_token == session_token_hashed)
    auth_session: AuthSession = await session.scalar(stmt)

    if auth_session:
        await session.delete(auth_session)
        await session.commit()

    response.delete_cookie(
        key="session_token",
        path="/api",
        secure=True,
        httponly=True,
        samesite="lax",
    )
