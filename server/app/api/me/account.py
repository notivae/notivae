# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import uuid
from fastapi import APIRouter, Request, BackgroundTasks, Depends, Body
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_async_session, rate_limited
from app.core.reusables.verification_mail import send_verification_email
from app.db.models import User, UserAvatar

router = APIRouter()


class AccountResponse(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    email_verified: bool
    name: str
    display_name: str | None
    is_system_admin: bool

    has_avatar: bool
    avatar_blurhash: str | None


@router.get(
    path='/account',
    response_model=AccountResponse,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def get_me(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
):
    stmt = sql.select(UserAvatar.blurhash).where(UserAvatar.owner_id == user.id)
    blurhash = await session.scalar(stmt)

    return AccountResponse(
        id=user.id,
        email=user.email,
        email_verified=user.email_verified,
        name=user.name,
        display_name=user.display_name,
        is_system_admin=user.is_system_admin,
        has_avatar=blurhash is not None,
        avatar_blurhash=blurhash,
    )


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
