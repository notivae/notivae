# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from fastapi import APIRouter, Depends
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user
from app.core.structures.oidc import UserInfo
from app.db.models import User, AuthIdentity


router = APIRouter()


class AuthIdentityResponse(pydantic.BaseModel):
    provider: str
    userinfo: UserInfo


@router.get("/auth-identities", response_model=t.List[AuthIdentityResponse])
async def get_me(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    stmt = sql.select(AuthIdentity).where(AuthIdentity.user_id == user.id)
    identities: t.Iterable[AuthIdentity] = await session.scalars(stmt)
    return identities
