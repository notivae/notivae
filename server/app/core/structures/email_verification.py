# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from pydantic import BaseModel, field_serializer


__all__ = ['EmailVerificationClaims']


class EmailVerificationClaims(BaseModel):
    sub: str
    exp: dt.datetime
    purpose: t.Literal["email-verification"]

    @field_serializer("exp")
    def __serialize_exp(self, exp: dt.datetime) -> int:
        return int(exp.timestamp())
