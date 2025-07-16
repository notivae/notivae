# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Response, status, Depends
from app.core.dependencies import rate_limited


router = APIRouter()


@router.post(
    path='/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def logout(response: Response) -> None:

    # todo: remove session from database

    response.delete_cookie(
        key="session_token",
        path="/api",
        secure=True,
        httponly=True,
        samesite="lax",
    )
