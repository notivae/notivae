# -*- coding=utf-8 -*-
r"""

"""
import enum
import sqlalchemy as sql
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

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)

    recipient_id = sql.Column(sql.Uuid, sql.ForeignKey('users.id'), nullable=False, index=True)
    title = sql.Column(sql.String(255), nullable=False)
    message = sql.Column(sql.Text, nullable=False)

    category = sql.Column(sql.String(255), nullable=False)
    status = sql.Column(sql.Enum(NotificationStatus), nullable=False, default=NotificationStatus.unread)

    created_at = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    expires_at = sql.Column(sql.DateTime(timezone=True), nullable=True)

    context = sql.Column(sql.JSON, nullable=True)
