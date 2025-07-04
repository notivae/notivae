# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Response, status


router = APIRouter()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:

    response.delete_cookie(
        key="session_token",
        secure=True,
        httponly=True,
        samesite="lax",
    )
