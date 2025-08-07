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
from app.core.dependencies import get_async_session, rate_limited

router = APIRouter()
logger: structlog.BoundLogger = structlog.get_logger()


class PydanticLogEntry(pydantic.BaseModel):
    level: int
    module: str
    lineno: int
    message: str
    context: dict
    timestamp: dt.datetime


@router.get(
    path='/',
    response_model=t.List[PydanticLogEntry],
    dependencies=[Depends(rate_limited(capacity=10, refill_rate=10/60))],
)
async def logs_query(
        session: AsyncSession = Depends(get_async_session),
        level: int = Query(default=logging.INFO, ge=logging.NOTSET, le=logging.CRITICAL),
        module: str = Query(default=None),
        limit: int = Query(default=50, ge=1, le=500),
        offset: int = Query(default=0, ge=0),
):
    logger.info("logs-query")
    stmt = sql.select(LogEntry)

    if level:
        stmt = stmt.where(LogEntry.level >= level)
    if module:
        stmt = stmt.where(LogEntry.module == module)

    stmt = stmt\
        .order_by(LogEntry.timestamp.desc()) \
        .offset(offset) \
        .limit(limit)

    return (await session.scalars(stmt)).all()
