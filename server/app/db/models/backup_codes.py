# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ..base import Base


__all__ = ['BackupCode']


class BackupCode(Base):
    __tablename__ = "backup_codes"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(sql.String, nullable=False)
    used: Mapped[bool] = mapped_column(sql.Boolean, nullable=False, default=False)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
