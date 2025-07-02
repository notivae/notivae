# -*- coding=utf-8 -*-
r"""

"""
import datetime
import sqlalchemy as sql
from ..base import Base


__all__ = ['Session']


class Session(Base):
    __tablename__ = "sessions"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hashed_token = sql.Column(sql.String, nullable=False, index=True)

    user_agent = sql.Column(sql.String, nullable=False)
    ip_address = sql.Column(sql.String, nullable=False)

    created_at = sql.Column(sql.DateTime(timezone=True), server_default=sql.func.now())
    expires_at = sql.Column(sql.DateTime(timezone=True), nullable=False, default=lambda: datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30))
    revoked = sql.Column(sql.Boolean, nullable=False, default=False)
