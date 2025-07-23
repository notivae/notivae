# -*- coding=utf-8 -*-
r"""

"""
import structlog
from fastapi import APIRouter, HTTPException, status, Depends, Path
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, Notification


router = APIRouter()
logger = structlog.get_logger()


@router.delete(
    path='/{notification_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=4/60))],
)
async def delete_notification(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        notification_id: int = Path(),
):
    stmt = sql.select(Notification).where(Notification.id == notification_id)
    notification: Notification = await session.scalar(stmt)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.recipient_id != auth_session.user_id:
        logger.warning(
            f"User {auth_session.user_id} attempted to delete a notification of {notification.recipient_id}",
            user_id=auth_session.user_id,
            recipient_id=notification.recipient_id,
            notification_id=notification.id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no permission to delete this notification",
        )

    await session.delete(notification)
    await session.commit()
