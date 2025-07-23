# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from fastapi import APIRouter, status, Depends, Body
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.db.models import User, Notification, NotificationCategory


CHUNK_SIZE = 100


router = APIRouter()


class BroadcastMessageRequest(pydantic.BaseModel):
    title: str
    message: str
    category: str = NotificationCategory.SYSTEM
    expires_at: t.Optional[dt.datetime]


@router.post(
    path='/broadcast',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def broadcast(
        session: AsyncSession = Depends(get_async_session),
        form: BroadcastMessageRequest = Body(),
) -> None:
    offset = 0

    while True:
        stmt = sql.select(User.id).order_by(User.id).limit(CHUNK_SIZE).offset(offset)
        user_ids: t.List[int] = list(await session.scalars(stmt))
        if not user_ids:
            break

        notifications = [
            Notification(
                recipient_id=user_id,
                title=form.title,
                message=form.message,
                category=form.category,
                expires_at=form.expires_at,
            )
            for user_id in user_ids
        ]
        session.add_all(notifications)

        # todo: redis publish (for ws)
        # todo: mail if-enabled

        offset += len(user_ids)

    await session.commit()
