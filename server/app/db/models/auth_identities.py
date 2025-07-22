# -*- coding=utf-8 -*-
r"""

"""
import sqlalchemy as sql
from ..base import Base


__all__ = ['AuthIdentity']


class AuthIdentity(Base):
    __tablename__ = "auth_identities"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = sql.Column(sql.String, nullable=False)
    provider_user_id = sql.Column(sql.String, nullable=False)
    provider_email = sql.Column(sql.String, nullable=False)
    userinfo = sql.Column(sql.JSON, nullable=True)
    context = sql.Column(sql.JSON, nullable=True)

    created_at = sql.Column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    __table_args__ = (
        sql.UniqueConstraint("user_id", "provider", "provider_user_id"),
    )
