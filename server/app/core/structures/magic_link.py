# -*- coding=utf-8 -*-
r"""

"""
from uuid import UUID
import typing as t
import datetime as dt
from pydantic import BaseModel, field_serializer


__all__ = ['MagicLinkClaims']


class MagicLinkClaims(BaseModel):
    sub: UUID
    exp: dt.datetime
    jti: UUID
    aud: t.Literal["magic-link"]

    @field_serializer("exp")
    def __serialize_exp(self, exp: dt.datetime) -> int:
        return int(exp.timestamp())
