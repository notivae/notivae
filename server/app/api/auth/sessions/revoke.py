# -*- coding=utf-8 -*-
r"""

"""
import structlog
from fastapi import APIRouter, status, Depends, Body
import sqlalchemy as sql
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user, get_current_auth_session, rate_limited
from app.db.models import User, AuthSession


router = APIRouter()
logger = structlog.get_logger()


class RevokeSessionsRequest(BaseModel):
    session_ids: list[int]


@router.post(
    path="/revoke",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=1/10))],
)
async def session_revoke(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user),
        current_session: AuthSession = Depends(get_current_auth_session),
        form: RevokeSessionsRequest = Body(),
):
    logger.info("Revoking sessions", user_id=user.id, session_ids=form.session_ids)

    stmt = (
        sql.update(AuthSession)
        .where(AuthSession.user_id == user.id, AuthSession.id != current_session.id, AuthSession.id.in_(form.session_ids))
        .values(revoked=True)
    )
    await session.execute(stmt)
    await session.commit()
