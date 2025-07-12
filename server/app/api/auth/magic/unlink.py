# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends
import sqlalchemy as sql
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.models import User, AuthIdentity
from app.core.dependencies import get_async_session, get_current_user


router = APIRouter()


@router.post("/unlink", status_code=status.HTTP_204_NO_CONTENT)
async def auth_local_unlink(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
) -> None:

    stmt = sql.select(sql.func.count()).where(AuthIdentity.user_id == user.id)
    number_auth_identities = await session.scalar(stmt)
    if number_auth_identities <= 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can't delete your last method of authentication",
        )

    stmt = sql.delete(AuthIdentity) \
        .where(AuthIdentity.provider == "magic", AuthIdentity.user_id == user.id)
    await session.execute(stmt)
    await session.commit()
