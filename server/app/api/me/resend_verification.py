# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends, Request, BackgroundTasks
from app.core.reusables.verification_mail import send_verification_email
from app.db.models import User
from app.core.dependencies import rate_limited, get_current_user


router = APIRouter()


@router.post(
    path="/resend-verification",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=3, refill_rate=1/300))],
)
async def resend_verification(
        request: Request,
        background_tasks: BackgroundTasks,
        user: User = Depends(get_current_user),
):
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already verified",
        )

    background_tasks.add_task(send_verification_email, request=request, user=user)
