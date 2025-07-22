# -*- coding=utf-8 -*-
r"""

"""
import sqlalchemy as sql
from ..base import Base


__all__ = ['BackupCode']


class BackupCode(Base):
    __tablename__ = "backup_codes"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code = sql.Column(sql.String, nullable=False)
    used = sql.Column(sql.Boolean, nullable=False, default=False)

    created_at = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
