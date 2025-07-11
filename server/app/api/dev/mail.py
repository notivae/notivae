# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Depends, status, HTTPException
from app.db.models import User
from app.core.dependencies import get_current_user
from app.services.mail import SUPPORTED, TestParameters, send_test_email


router = APIRouter(prefix="/mail")


@router.post("/test", status_code=status.HTTP_204_NO_CONTENT)
async def post_mail_test(
        user: User = Depends(get_current_user),
):
    if not SUPPORTED:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Mail service is not supported")

    await send_test_email(
        to=user.email,
        parameters=TestParameters(),
    )
