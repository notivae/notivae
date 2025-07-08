# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import datetime as dt
from pydantic import BaseModel, field_serializer


__all__ = ['AccountApprovalClaims']


class AccountApprovalClaims(BaseModel):
    sub: str
    exp: dt.datetime
    purpose: t.Literal["account-approval"]

    @field_serializer("exp")
    def __serialize_exp(self, exp: dt.datetime) -> int:
        return int(exp.timestamp())
