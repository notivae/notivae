# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import uuid
from fastapi import APIRouter, Request, BackgroundTasks, Depends, Body
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_async_session
from app.core.reusables.verification_mail import send_verification_email
from app.db.models import User


router = APIRouter()


class UserMeResponse(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    name: str
    display_name: t.Optional[str]


@router.get("/me", response_model=UserMeResponse)
async def get_me(
        user: User = Depends(get_current_user),
):
    return user


class UserMePartialRequest(pydantic.BaseModel):
    email: t.Optional[pydantic.EmailStr] = None
    name: t.Optional[str] = None
    display_name: t.Optional[str] = None


@router.patch("/me", response_model=UserMeResponse)
async def patch_me(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        changed: UserMePartialRequest = Body()
):
    if 'email' in changed.model_fields_set:
        user.email = changed.email
        user.email_verified = False
    if 'name' in changed.model_fields_set:
        user.name = changed.name
    if 'display_name' in changed.model_fields_set:
        user.display_name = changed.display_name
    await session.commit()
    await session.refresh(user)

    if 'email' in changed.model_fields_set:
        background_tasks.add_task(send_verification_email, request=request, user=user)

    return user
