# -*- coding=utf-8 -*-
r"""

"""
import uuid
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


__all__ = ['UserAvatar']


class UserAvatar(Base):
    __tablename__ = 'users_avatars'

    id: Mapped[int] = mapped_column(sql.BigInteger, primary_key=True, autoincrement=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(sql.Uuid, sql.ForeignKey("users.id", ondelete="CASCADE"), index=True, unique=True, nullable=False)

    storage_path: Mapped[str] = mapped_column(sql.String, nullable=False)
    sha256_hash: Mapped[str] = mapped_column(sql.String(64), nullable=False)
    blurhash: Mapped[str] = mapped_column(sql.String, nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(sql.DateTime(timezone=True), nullable=False, server_default=sql.func.now())
