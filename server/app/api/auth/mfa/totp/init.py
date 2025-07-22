# -*- coding=utf-8 -*-
r"""

"""
import pyotp
from fastapi import APIRouter, HTTPException, status, Depends, Request, BackgroundTasks
from pydantic import BaseModel
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, MFACredentials, BackupCode
from app.core.dependencies import get_async_session, get_current_user, rate_limited
from app.core.reusables.mfa_enabled import send_mfa_enabled_email


router = APIRouter()


class TwoFASetupResponse(BaseModel):
    secret: str
    provisioning_uri: str


@router.post(
    path='/init',
    response_model=TwoFASetupResponse,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/300))],
)
async def mfa_totp_init(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
):
    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == user.id, MFACredentials.method == "totp")
    existing: MFACredentials = await session.scalar(stmt)
    if existing:
        if existing.confirmed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="TOTP MFA credentials already configured",
            )
        await session.delete(existing)

    stmt = sql.select(BackupCode).where(BackupCode.user_id == user.id, BackupCode.used != True)
    existing: BackupCode = await session.scalar(stmt)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="MFA Backup Codes not configured",
        )

    secret = pyotp.random_base32()
    provisioning_uri = pyotp.TOTP(secret).provisioning_uri(name=user.name, issuer_name="Notivae")

    session.add(MFACredentials(
        user_id=user.id,
        method="totp",
        secret=secret,
    ))
    await session.commit()

    background_tasks.add_task(send_mfa_enabled_email, request=request, user=user)

    return TwoFASetupResponse(
        secret=secret,
        provisioning_uri=provisioning_uri,
    )
