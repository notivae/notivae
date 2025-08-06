# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ..base import Base


__all__ = ['MFACredentials']


class MFACredentials(Base):
    __tablename__ = "mfa_credentials"

    user_id: Mapped[UUID] = mapped_column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    method: Mapped[str] = mapped_column(sql.String, index=True, primary_key=True, nullable=False)
    secret: Mapped[str] = mapped_column(sql.String, nullable=True)
    confirmed: Mapped[bool] = mapped_column(sql.Boolean, index=True, nullable=False, default=False)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
