# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from fastapi import APIRouter, Depends
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user, rate_limited
from app.core.structures.oidc import OpenIdUserInfo
from app.db.models import User, AuthIdentity


router = APIRouter()


class AuthIdentityResponseItem(pydantic.BaseModel):
    provider: str
    provider_user_id: str
    provider_email: str
    userinfo: t.Optional[OpenIdUserInfo]


@router.get(
    path='/auth-identities',
    response_model=t.List[AuthIdentityResponseItem],
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=5/60))],
)
async def get_auth_identities(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    stmt = sql.select(AuthIdentity).where(AuthIdentity.user_id == user.id)
    identities: t.Iterable[AuthIdentity] = await session.scalars(stmt)
    return identities
