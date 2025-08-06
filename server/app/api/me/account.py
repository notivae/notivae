# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import uuid
from fastapi import APIRouter, Request, BackgroundTasks, Depends, Body
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_async_session, rate_limited
from app.core.reusables.verification_mail import send_verification_email
from app.db.models import User


router = APIRouter()


class AccountResponse(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    email_verified: bool
    name: str
    display_name: t.Optional[str]
    is_system_admin: bool


@router.get(
    path='/account',
    response_model=AccountResponse,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def get_me(
        user: User = Depends(get_current_user),
):
    return user


class AccountPartialRequest(pydantic.BaseModel):
    email: t.Optional[pydantic.EmailStr] = None
    name: t.Optional[str] = None
    display_name: t.Optional[str] = None


@router.patch(
    path='/account',
    response_model=AccountResponse,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=5/300))],
)
async def patch_me(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        changes: AccountPartialRequest = Body()
):
    if 'email' in changes.model_fields_set and changes.email != user.email:
        user.email = str(changes.email)
        user.email_verified = False
    if 'name' in changes.model_fields_set and changes.name != user.name:
        user.name = changes.name
    if 'display_name' in changes.model_fields_set and changes.display_name != user.display_name:
        user.display_name = changes.display_name
    await session.commit()
    await session.refresh(user)

    if 'email' in changes.model_fields_set and not user.email_verified:
        background_tasks.add_task(send_verification_email, request=request, user=user)

    return user
