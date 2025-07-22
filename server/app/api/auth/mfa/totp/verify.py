# -*- coding=utf-8 -*-
r"""

"""
import pyotp
from fastapi import APIRouter, HTTPException, status, Depends, Form
from pydantic import BaseModel
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, MFACredentials


router = APIRouter()


class VerifyRequest(BaseModel):
    otp: str


@router.post(
    path='/verify',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/300))],
)
async def mfa_totp_verify(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        form: VerifyRequest = Form(),
):
    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == auth_session.user_id, MFACredentials.method == "totp")
    mfa_credentials: MFACredentials = await session.scalar(stmt)

    if mfa_credentials is None or not mfa_credentials.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP MFA is not configured or confirmed",
        )

    if not pyotp.TOTP(mfa_credentials.secret).verify(otp=form.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )

    auth_session.is_mfa_authenticated = True
    await session.commit()
