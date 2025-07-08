# -*- coding=utf-8 -*-
r"""

"""
from passlib.context import CryptContext


__all__ = ['verify_password', 'hash_password']


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> bytes:
    return pwd_context.hash(plain_password)
