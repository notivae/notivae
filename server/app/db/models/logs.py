# -*- coding=utf-8 -*-
r"""

"""
import sqlalchemy as sql
from ..base import Base


__all__ = ['LogEntry']


class LogEntry(Base):
    __tablename__ = "log_entries"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    level = sql.Column(sql.SmallInteger, nullable=False)
    module = sql.Column(sql.String, nullable=False)
    lineno = sql.Column(sql.Integer, nullable=False)
    message = sql.Column(sql.Text, nullable=False)
    context = sql.Column(sql.JSON, nullable=True)
    timestamp = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
