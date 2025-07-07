# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import uuid
from fastapi import APIRouter, Depends, Body
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_async_session
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
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        changed: UserMePartialRequest = Body()
):
    if 'email' in changed.model_fields_set:
        user.email = changed.email
        # todo: re-validation request
    if 'name' in changed.model_fields_set:
        user.name = changed.name
    if 'display_name' in changed.model_fields_set:
        user.display_name = changed.display_name
    await session.commit()
    await session.refresh(user)

    return user
