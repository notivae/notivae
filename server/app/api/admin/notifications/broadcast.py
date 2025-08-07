# -*- coding=utf-8 -*-
r"""

"""
import json
import asyncio
import typing as t
import datetime as dt
from uuid import UUID
import structlog
from fastapi import APIRouter, status, Depends, Body, Request
from fastapi.encoders import jsonable_encoder
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.db.models import User, Notification, NotificationCategory
from app.core.redis import redis_client
from app.services.mail import send_new_notification_email, NewNotificationParameters


CHUNK_SIZE = 100


router = APIRouter()
logger = structlog.get_logger()


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
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        form: BroadcastMessageRequest = Body(),
) -> None:
    offset = 0

    while True:
        stmt = sql.select(User.id, User.email, User.email_verified).limit(CHUNK_SIZE).offset(offset)
        users: t.Sequence[sql.Row[tuple[UUID, str, bool]]] = (await session.execute(stmt)).all()
        if not users:
            break

        tasks: list[asyncio.Future] = []

        for user_id, user_email, user_is_email_verified in users:
            notification = Notification(
                recipient_id=user_id,
                title=form.title,
                message=form.message,
                category=form.category,
                expires_at=form.expires_at,
            )
            session.add(notification)
            await session.flush((notification,))

            ws_json = json.dumps(dict(
                type="notification",
                payload=jsonable_encoder(notification),
            ))
            coro = redis_client.publish(f"ws:{user_id}:notifications", ws_json)
            tasks.append(asyncio.create_task(coro))

            # todo: mail only if-enabled
            if user_is_email_verified:
                parameters = NewNotificationParameters(
                    title=notification.title,
                    message=notification.message,
                    category=notification.category,
                    expires_at=notification.expires_at,
                )
                coro = send_new_notification_email(to=user_email, parameters=parameters, request=request)
                tasks.append(asyncio.create_task(coro))

        done, _ = await asyncio.wait(tasks)
        for task in done:
            exc = task.exception()
            if exc:
                logger.error(f"{type(exc)}: {exc}", exc_info=exc)

        await session.commit()

        offset += len(users)
