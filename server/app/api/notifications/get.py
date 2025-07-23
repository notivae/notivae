# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
import structlog
from fastapi import APIRouter, Depends, Query
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, Notification
from ._models import NotificationResponseModel


router = APIRouter()
logger = structlog.get_logger()


@router.get(
    path='/',
    response_model=t.List[NotificationResponseModel],
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=4/60))],
)
async def get_notifications(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        limit: int = Query(default=50, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
):
    now = dt.datetime.now(dt.UTC)

    stmt = sql.select(Notification)\
        .where(
            Notification.recipient_id is auth_session.user_id,
            sql.or_(Notification.expires_at.is_(None), Notification.expires_at > now),
        )\
        .order_by(Notification.created_at.desc()) \
        .offset(offset) \
        .limit(limit)

    return (await session.scalars(stmt)).all()
