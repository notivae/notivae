# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user, rate_limited
from app.db.models import User, BackupCode
from app.core.security.mfa_backup_codes import generate_backup_codes


router = APIRouter()


class MFABackupRegenerateResponse(BaseModel):
    backup_codes: t.List[str]


@router.post(
    path='/regenerate',
    response_model=MFABackupRegenerateResponse,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/300))],
)
async def mfa_backup_regenerate(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
):
    stmt = sql.delete(BackupCode).where(BackupCode.user_id == user.id)
    await session.execute(stmt)

    backup_codes = generate_backup_codes(count=10)
    for code in backup_codes:
        session.add(BackupCode(
            user_id=user.id,
            code=code,
        ))

    await session.commit()

    return MFABackupRegenerateResponse(
        backup_codes=backup_codes,
    )
