# -*- coding=utf-8 -*-
r"""
todo: batch processing
"""
import typing as t
import structlog
from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, Notification, NotificationStatus
from ._models import NotificationResponseModel


router = APIRouter()
logger = structlog.get_logger()


class NotificationPartialRequest(pydantic.BaseModel):
    status: t.Optional[NotificationStatus] = None


@router.patch(
    path='/{notification_id}',
    response_model=NotificationResponseModel,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=4/60))],
)
async def patch_notification(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        notification_id: int = Path(),
        changes: NotificationPartialRequest = Body(),
):
    stmt = sql.select(Notification).where(Notification.id == notification_id)
    notification: Notification = await session.scalar(stmt)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.recipient_id != auth_session.user_id:
        logger.warning(f"User {auth_session.user_id} attempted to delete a notification of {notification.recipient_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no permission to delete this notification",
        )

    if 'status' in changes.model_fields_set:
        notification.status = changes.status

    if session.is_modified(notification):
        await session.commit()
        await session.refresh(notification)

    return notification
