# -*- coding=utf-8 -*-
r"""

"""
import uuid
import datetime as dt
from jose import jwt
from app.config import SETTINGS
from ..structures.email_verification import EmailVerificationClaims


__all__ = ['generate_email_verification_token', 'parse_email_verification_token']


def generate_email_verification_token(user_id: uuid.UUID) -> str:
    claims = EmailVerificationClaims(
        sub=str(user_id),
        exp=dt.datetime.now(dt.UTC) + dt.timedelta(minutes=30),
        purpose="email-verification",
    )
    return jwt.encode(
        claims=claims.model_dump(mode='json'),
        key=SETTINGS.SECURITY.SECRET_KEY,
        algorithm=SETTINGS.SECURITY.JWT_ALGORITHM,
    )


def parse_email_verification_token(token: str, ignore_expired: bool = False) -> EmailVerificationClaims:
    return EmailVerificationClaims.model_validate(
        jwt.decode(
            token=token,
            key=SETTINGS.SECURITY.SECRET_KEY,
            algorithms=[SETTINGS.SECURITY.JWT_ALGORITHM],
            options={ 'verify_exp': not ignore_expired },
        )
    )
