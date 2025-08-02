# -*- coding=utf-8 -*-
r"""

"""
from uuid import UUID
import typing as t
import datetime as dt
from pydantic import BaseModel, field_serializer


__all__ = ['LocalPasswordResetClaims']


class LocalPasswordResetClaims(BaseModel):
    sub: UUID
    exp: dt.datetime
    jti: UUID
    aud: t.Literal["local-password-reset"]

    @field_serializer("exp")
    def __serialize_exp(self, exp: dt.datetime) -> int:
        return int(exp.timestamp())
