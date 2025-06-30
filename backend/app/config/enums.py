# -*- coding=utf-8 -*-
r"""

"""
import enum


__all__ = [
    'AccountCreationMode',
]


class AccountCreationMode(str, enum.Enum):
    CLOSED = "closed"
    RESTRICTED = "restricted"
    OPEN = "open"
