# -*- coding=utf-8 -*-
r"""

"""
from uuid import UUID
import datetime as dt
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.db.models import User


router = APIRouter()


class UserItem(BaseModel):
    id: UUID
    email: str
    email_verified: bool
    name: str
    display_name: str | None
    is_approved: bool
    is_system_admin: bool
    created_at: dt.datetime


@router.get(
    path="/list",
    response_model=list[UserItem],
)
async def admin_list_users(
        session: AsyncSession = Depends(get_async_session),
        limit: int = Query(default=50, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
):
    stmt = sql.select(User) \
        .order_by(User.name.asc()) \
        .offset(offset) \
        .limit(limit)
    return await session.scalars(stmt)
