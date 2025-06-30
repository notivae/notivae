# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, status, Depends
import sqlalchemy as sql
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.models import User, AuthIdentity
from app.core.dependencies import get_async_session, get_current_user


router = APIRouter()


@router.post("/unlink", status_code=status.HTTP_204_NO_CONTENT)
async def oidc_unlink(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
) -> None:
    stmt = sql.delete(AuthIdentity) \
        .where(AuthIdentity.provider == "oidc", AuthIdentity.user_id == user.id)
    await session.execute(stmt)
    await session.commit()
