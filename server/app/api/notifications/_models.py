# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from pydantic import BaseModel
from app.db.models import NotificationStatus


__all__ = ['NotificationResponseModel']


class NotificationResponseModel(BaseModel):
    id: int
    title: str
    message: str
    status: NotificationStatus
    created_at: dt.datetime
    expires_at: t.Optional[dt.datetime]
    context: t.Optional[dict]
