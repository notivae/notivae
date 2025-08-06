# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
import sqlalchemy as sql
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, AuthSession
from app.core.dependencies import get_async_session, get_current_user, get_current_auth_session, rate_limited


router = APIRouter()


class SessionItem(BaseModel):
    id: int
    is_current: bool

    user_agent: str
    ip_address: str

    created_at: dt.datetime
    expires_at: dt.datetime
    revoked: bool


@router.get(
    path="/",
    response_model=list[SessionItem],
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/10))],
)
async def get_sessions(
        session: AsyncSession = Depends(get_async_session),
        current_auth_session: AuthSession = Depends(get_current_auth_session),
        user: User = Depends(get_current_user),
):
    stmt = sql.select(AuthSession).where(AuthSession.user_id == user.id)
    auth_sessions: list[AuthSession] = list(await session.scalars(stmt))

    return [
        SessionItem(**jsonable_encoder(sess), is_current=sess.id == current_auth_session.id)
        for sess in auth_sessions
    ]
