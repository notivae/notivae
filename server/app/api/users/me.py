# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import uuid
from fastapi import APIRouter, Depends
import pydantic
from app.core.dependencies import get_current_user


router = APIRouter()


class UserMeResponse(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    name: str
    display_name: t.Optional[str]


@router.get("/me", response_model=UserMeResponse)
async def get_me(user = Depends(get_current_user)):
    return user
