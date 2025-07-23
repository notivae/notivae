# -*- coding=utf-8 -*-
r"""

"""
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from datetime import datetime
from ..base import Base


__all__ = ['AuthIdentity']


class AuthIdentity(Base):
    __tablename__ = "auth_identities"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider: Mapped[str] = mapped_column(sql.String, nullable=False)
    provider_user_id: Mapped[str] = mapped_column(sql.String, nullable=False)
    provider_email: Mapped[str] = mapped_column(sql.String, nullable=False)
    userinfo: Mapped[dict] = mapped_column(sql.JSON, nullable=True)
    context: Mapped[dict] = mapped_column(sql.JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    __table_args__ = (
        sql.UniqueConstraint("user_id", "provider", "provider_user_id"),
    )
