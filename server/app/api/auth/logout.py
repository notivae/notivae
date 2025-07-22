# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import rate_limited, get_async_session, get_current_auth_session_optional
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
        auth_session: AuthSession = Depends(get_current_auth_session_optional),
) -> None:

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
