# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ..base import Base


__all__ = ['AuthSession']


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hashed_token: Mapped[str] = mapped_column(sql.String, nullable=False, index=True)

    user_agent: Mapped[str] = mapped_column(sql.String, nullable=False)
    ip_address: Mapped[str] = mapped_column(sql.String, nullable=False)

    is_mfa_authenticated: Mapped[bool | None] = mapped_column(sql.Boolean, nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    expires_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, default=lambda: dt.datetime.now(dt.UTC) + dt.timedelta(days=30))
    revoked: Mapped[bool] = mapped_column(sql.Boolean, nullable=False, default=False)

    @staticmethod
    def is_valid(instance: 'AuthSession') -> bool:
        return not (
            instance is None
            or instance.revoked
            or instance.expires_at < dt.datetime.now(dt.UTC)
        )
