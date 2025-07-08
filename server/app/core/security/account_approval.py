# -*- coding=utf-8 -*-
r"""

"""
import uuid
import datetime as dt
from jose import jwt
from app.config import SETTINGS
from ..structures.account_approval import AccountApprovalClaims


__all__ = ['generate_account_approval_token', 'parse_account_approval_token']


def generate_account_approval_token(user_id: uuid.UUID) -> str:
    claims = AccountApprovalClaims(
        sub=str(user_id),
        exp=dt.datetime.now(dt.UTC) + dt.timedelta(days=1),
        purpose="account-approval",
    )
    return jwt.encode(
        claims=claims.model_dump(mode='json'),
        key=SETTINGS.SECURITY.SECRET_KEY,
        algorithm=SETTINGS.SECURITY.JWT_ALGORITHM,
    )


def parse_account_approval_token(token: str) -> AccountApprovalClaims:
    return AccountApprovalClaims.model_validate(
        jwt.decode(
            token=token,
            key=SETTINGS.SECURITY.SECRET_KEY,
            algorithms=[SETTINGS.SECURITY.JWT_ALGORITHM],
        )
    )
