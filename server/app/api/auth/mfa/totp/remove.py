# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, MFACredentials
from app.core.dependencies import get_async_session, get_current_user, rate_limited


router = APIRouter()


@router.delete(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=2, refill_rate=1/60))],
)
async def mfa_totp_delete(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
):
    stmt = sql.select(MFACredentials).where(MFACredentials.user_id == user.id, MFACredentials.method == "totp")
    mfa_credentials: MFACredentials = await session.scalar(stmt)

    if mfa_credentials is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP MFA not configured",
        )

    await session.delete(mfa_credentials)
    await session.commit()
