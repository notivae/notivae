# -*- coding=utf-8 -*-
r"""

"""
import secrets
import hashlib
from app.config import SETTINGS


__all__ = ['generate_session_token', 'hash_session_token']


def generate_session_token() -> str:
    return secrets.token_urlsafe(nbytes=SETTINGS.SECURITY.SESSION_TOKEN_NBYTES)


def hash_session_token(session_token: str) -> str:
    return hashlib.sha256(session_token.encode('utf-8')).hexdigest()
