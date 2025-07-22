# -*- coding=utf-8 -*-
r"""

"""
import pyotp
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import BaseModel
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, MFACredentials


router = APIRouter()


class MfaTotpConfirmRequest(BaseModel):
    totp: str


@router.post(
    path='/confirm',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/60))],
)
async def mfa_totp_confirm(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        form: MfaTotpConfirmRequest = Body()
):
    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == auth_session.user_id, MFACredentials.method == "totp")
    mfa_credentials: MFACredentials = await session.scalar(stmt)
    if not mfa_credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP MFA not configured",
        )

    if not pyotp.TOTP(mfa_credentials.secret).verify(form.totp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP MFA verification failed",
        )

    mfa_credentials.confirmed = True
    auth_session.is_mfa_authenticated = True
    await session.commit()
