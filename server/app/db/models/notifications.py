# -*- coding=utf-8 -*-
r"""

"""
import enum
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ..base import Base


__all__ = ['Notification', 'NotificationStatus', 'NotificationCategory']


class NotificationStatus(enum.Enum):
    unread = "unread"
    read = "read"
    archived = "archived"


class NotificationCategory:  # not enum
    SYSTEM = "system"


class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)

    recipient_id: Mapped[UUID] = mapped_column(sql.Uuid, sql.ForeignKey('users.id'), nullable=False, index=True)
    title: Mapped[str] = mapped_column(sql.String(255), nullable=False)
    message: Mapped[str] = mapped_column(sql.Text, nullable=False)

    category: Mapped[str] = mapped_column(sql.String(255), nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(sql.Enum(NotificationStatus), nullable=False, default=NotificationStatus.unread)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    expires_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=True)

    context: Mapped[dict | None] = mapped_column(sql.JSON, nullable=True)
