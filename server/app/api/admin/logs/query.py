# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import logging
import datetime as dt
import structlog
import pydantic
from fastapi import APIRouter, Query, Depends
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import LogEntry
from app.core.dependencies import get_async_session


router = APIRouter()
logger: structlog.BoundLogger = structlog.get_logger()


class PydanticLogEntry(pydantic.BaseModel):
    level: int
    event: str
    message: t.Optional[str]
    context: t.Optional[dict]
    timestamp: dt.datetime


@router.get('/query', response_model=t.List[PydanticLogEntry])
async def logs_live(
        session: AsyncSession = Depends(get_async_session),
        level: int = Query(default=logging.INFO, ge=logging.NOTSET, le=logging.CRITICAL),
        event: str = Query(default=None),
        limit: int = Query(default=50, ge=1, le=500),
        offset: int = Query(default=0, ge=0),
):
    logger.info("logs-query")
    stmt = sql.select(LogEntry)

    if level:
        stmt = stmt.where(LogEntry.level >= level)
    if event:
        stmt = stmt.where(LogEntry.event.ilike(f"%{event}%"))

    stmt = stmt\
        .order_by(LogEntry.timestamp.desc()) \
        .offset(offset) \
        .limit(limit)

    return (await session.scalars(stmt)).all()
