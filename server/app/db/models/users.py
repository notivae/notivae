# -*- coding=utf-8 -*-
r"""

"""
import uuid
import sqlalchemy as sql
from ..base import Base


__all__ = ['User']


class User(Base):
    __tablename__ = "users"

    id = sql.Column(sql.Uuid, primary_key=True, default=uuid.uuid4)
    email = sql.Column(sql.String, unique=True, nullable=False)
    name = sql.Column(sql.String, nullable=False)
    display_name = sql.Column(sql.String)

    is_approved = sql.Column(sql.Boolean, nullable=False, default=False)
    is_system_admin = sql.Column(sql.Boolean, nullable=False, default=False)

    created_at = sql.Column(sql.DateTime(timezone=True), server_default=sql.func.now())
