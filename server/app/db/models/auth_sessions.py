# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
import sqlalchemy as sql
from ..base import Base


__all__ = ['AuthSession']


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hashed_token = sql.Column(sql.String, nullable=False, index=True)

    user_agent = sql.Column(sql.String, nullable=False)
    ip_address = sql.Column(sql.String, nullable=False)

    is_mfa_authenticated: t.Optional[bool] = sql.Column(sql.Boolean, nullable=True)

    created_at = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    expires_at = sql.Column(sql.DateTime(timezone=True), nullable=False, default=lambda: dt.datetime.now(dt.UTC) + dt.timedelta(days=30))
    revoked = sql.Column(sql.Boolean, nullable=False, default=False)

    @staticmethod
    def is_valid(instance: 'AuthSession') -> bool:
        return not (
            instance is None
            or instance.revoked
            or instance.expires_at < dt.datetime.now(dt.UTC)
        )
