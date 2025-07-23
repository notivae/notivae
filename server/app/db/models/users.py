# -*- coding=utf-8 -*-
r"""

"""
import uuid
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


__all__ = ['User']


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(sql.Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(sql.String, nullable=False)
    email_verified: Mapped[bool] = mapped_column(sql.Boolean, nullable=False, default=False)
    name: Mapped[str] = mapped_column(sql.String, nullable=False)  # todo: merge with display_name?
    display_name: Mapped[str | None] = mapped_column(sql.String, nullable=True)

    is_approved: Mapped[bool] = mapped_column(sql.Boolean, nullable=False, default=False)
    is_system_admin: Mapped[bool] = mapped_column(sql.Boolean, nullable=False, default=False)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
