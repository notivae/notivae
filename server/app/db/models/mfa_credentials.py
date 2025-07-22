# -*- coding=utf-8 -*-
r"""

"""
import sqlalchemy as sql
from ..base import Base


__all__ = ['MFACredentials']


class MFACredentials(Base):
    __tablename__ = "mfa_credentials"

    user_id = sql.Column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    method = sql.Column(sql.String, primary_key=True, nullable=False)
    secret = sql.Column(sql.String, nullable=True)
    confirmed = sql.Column(sql.Boolean, nullable=False, default=False)

    created_at = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
