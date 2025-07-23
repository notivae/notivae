# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


__all__ = ['LogEntry']


class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True, autoincrement=True)
    level: Mapped[int] = mapped_column(sql.SmallInteger, nullable=False)
    module: Mapped[str] = mapped_column(sql.String, nullable=False)
    lineno: Mapped[int] = mapped_column(sql.Integer, nullable=False)
    message: Mapped[str] = mapped_column(sql.Text, nullable=False)
    context: Mapped[dict] = mapped_column(sql.JSON, nullable=True)
    timestamp: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
