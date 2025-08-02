# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
import uuid
from jose import jwt
from passlib.context import CryptContext
from app.config import SETTINGS
from app.core.structures.local import LocalPasswordResetClaims


__all__ = [
    'verify_password', 'hash_password',
    'generate_local_password_reset_token', 'parse_local_password_reset_token',
]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> bytes:
    return pwd_context.hash(plain_password)



def generate_local_password_reset_token(user_id: uuid.UUID) -> str:
    claims = LocalPasswordResetClaims(
        sub=user_id,
        exp=dt.datetime.now(dt.UTC) + dt.timedelta(minutes=15),
        jti=uuid.uuid4(),
        aud="local-password-reset",
    )
    return jwt.encode(
        claims=claims.model_dump(mode='json'),
        key=SETTINGS.SECURITY.SECRET_KEY,
        algorithm=SETTINGS.SECURITY.JWT_ALGORITHM,
    )


def parse_local_password_reset_token(token: str) -> LocalPasswordResetClaims:
    return LocalPasswordResetClaims.model_validate(
        jwt.decode(
            token=token,
            key=SETTINGS.SECURITY.SECRET_KEY,
            algorithms=[SETTINGS.SECURITY.JWT_ALGORITHM],
            audience="local-password-reset",
        )
    )
