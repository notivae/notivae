# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, status, BackgroundTasks, Request, Depends
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, rate_limited
from app.core.reusables.forgot_password import send_local_forgot_password_email
from app.db.models import AuthIdentity


router = APIRouter()


class LocalForgotPasswordRequest(pydantic.BaseModel):
    email: str


@router.post(
    path="/forgot-password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/30))],
)
async def auth_local_forgot_password(
        request: Request,
        background_tasks: BackgroundTasks,
        form: LocalForgotPasswordRequest,
        session: AsyncSession = Depends(get_async_session),
):
    stmt = sql.Select(AuthIdentity).where(AuthIdentity.provider == "local", AuthIdentity.provider_email == form.email)
    auth_identity: AuthIdentity = await session.scalar(stmt)
    if auth_identity:  # no fail to prevent email-probing
        background_tasks.add_task(send_local_forgot_password_email, request=request, user_id=auth_identity.user_id, user_email=auth_identity.provider_email)
