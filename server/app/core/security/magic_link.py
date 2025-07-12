# -*- coding=utf-8 -*-
r"""

"""
import uuid
import datetime as dt
from jose import jwt
from app.config import SETTINGS
from ..structures.magic_link import MagicLinkClaims


__all__ = ['generate_magic_link_token', 'parse_magic_link_token']


def generate_magic_link_token(user_id: uuid.UUID) -> str:
    claims = MagicLinkClaims(
        sub=user_id,
        exp=dt.datetime.now(dt.UTC) + dt.timedelta(minutes=15),
        jti=uuid.uuid4(),
        aud="magic-link",
    )
    return jwt.encode(
        claims=claims.model_dump(mode='json'),
        key=SETTINGS.SECURITY.SECRET_KEY,
        algorithm=SETTINGS.SECURITY.JWT_ALGORITHM,
    )


def parse_magic_link_token(token: str) -> MagicLinkClaims:
    return MagicLinkClaims.model_validate(
        jwt.decode(
            token=token,
            key=SETTINGS.SECURITY.SECRET_KEY,
            algorithms=[SETTINGS.SECURITY.JWT_ALGORITHM],
            audience="magic-link",
        )
    )
