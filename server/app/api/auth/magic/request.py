# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Request, Body, Depends, BackgroundTasks
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.dependencies import get_async_session, rate_limited
from app.db.models import User, AuthIdentity
from app.core.reusables.magic_link import send_magic_link_email


router = APIRouter()


class MagicRequestRequest(BaseModel):
    email: str


@router.post(
    path='/request',
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=3/60))],
)
async def magic_request(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        form: MagicRequestRequest = Body(),
):
    stmt = sql.select(User).where(User.email == form.email)
    user: User = await session.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User for this email not found",
        )
    if not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not approved",
        )

    stmt = sql.select(AuthIdentity).where(AuthIdentity.provider == "magic", AuthIdentity.user_id == user.id)
    auth_identity: AuthIdentity = await session.scalar(stmt)
    if not auth_identity:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Magic-Link is not configured for this user",
        )

    background_tasks.add_task(send_magic_link_email, request=request, user=user)
