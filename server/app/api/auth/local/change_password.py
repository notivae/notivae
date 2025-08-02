# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import BaseModel, Field
from jose import ExpiredSignatureError
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user_optional, rate_limited
from app.core.security.local import parse_local_password_reset_token
from app.db.models import User, AuthIdentity
from app.core.security.local import hash_password
from ._common import AuthLocalIdentityContext


router = APIRouter()


class ChangePasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=4)
    token: str = Field(None)


@router.post(
    path='/change-password',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/60))],
)
async def auth_local_change_password(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user_optional),
        changes: ChangePasswordRequest = Body(),
):
    if changes.token:  # passed token takes precedence over session cookie
        try:
            claims = parse_local_password_reset_token(changes.token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The token is expired",
            )
        stmt = sql.select(User).where(User.id == claims.sub)
        user: User = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication",
        )

    # todo: validate password strength

    stmt = sql.select(AuthIdentity).where(AuthIdentity.provider == "local", AuthIdentity.user_id == user.id)
    auth_identity: AuthIdentity = await session.scalar(stmt)
    if not auth_identity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Local Authentication does not exist for your account",
        )

    context = AuthLocalIdentityContext.model_validate(auth_identity.context)
    context.password_hashed = hash_password(changes.new_password)
    auth_identity.context = context.model_dump(mode='json')

    await session.commit()
