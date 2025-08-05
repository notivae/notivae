# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import BaseModel
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_auth_session, rate_limited
from app.db.models import AuthSession, BackupCode


router = APIRouter()


class VerifyRequest(BaseModel):
    backup_code: str


@router.post(
    path='/verify',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/60))],
)
async def mfa_backup_verify(
        session: AsyncSession = Depends(get_async_session),
        auth_session: AuthSession = Depends(get_current_auth_session),
        form: VerifyRequest = Body(),
):
    stmt = sql.select(BackupCode).where(BackupCode.user_id == auth_session.user_id, BackupCode.code == form.backup_code.upper())
    backup_code: BackupCode = await session.scalar(stmt)

    if backup_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown backup code",
        )
    if backup_code.used:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Backup code is already used",
        )

    backup_code.used = True
    auth_session.is_mfa_authenticated = True

    await session.commit()
