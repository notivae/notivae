# -*- coding=utf-8 -*-
r"""

"""
import asyncio
from fastapi import APIRouter, Depends
import pydantic
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user, rate_limited
from app.db.models import User, BackupCode, MFACredentials


router = APIRouter()


class MfaDetailsResponse(pydantic.BaseModel):
    backup_codes_remaining: int | None
    totp: bool


@router.get(
    path='/mfa-details',
    response_model=MfaDetailsResponse,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=5/60))],
)
async def get_mfa_details(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):

    async def fetch_backup_codes_remaining():
        stmt = sql.select(~BackupCode.used).where(
            BackupCode.user_id == user.id,
        )
        backup_codes_rows: list[bool] = list(await session.scalars(stmt))

        return sum(backup_codes_rows) if len(backup_codes_rows) else None

    async def fetch_mfa_methods():
        stmt = sql.select(MFACredentials.method).where(
            MFACredentials.user_id == user.id,
            MFACredentials.confirmed.is_(True),
        )
        return list(await session.scalars(stmt))

    backup_codes_remaining, confirmed_mfa_methods = await asyncio.gather(
        fetch_backup_codes_remaining(),
        fetch_mfa_methods(),
    )

    return MfaDetailsResponse(
        backup_codes_remaining=backup_codes_remaining,
        totp='totp' in confirmed_mfa_methods,
    )
