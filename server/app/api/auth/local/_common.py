# -*- coding=utf-8 -*-
r"""

"""
from pydantic import BaseModel


__all__ = ['AuthLocalIdentityContext']


class AuthLocalIdentityContext(BaseModel):
    password_hashed: bytes
