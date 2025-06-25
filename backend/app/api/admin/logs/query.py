# -*- coding=utf-8 -*-
r"""

"""
import logging
import structlog
from fastapi import APIRouter, Request, Query
import sqlalchemy as sql
from app.db.session import AsyncSessionLocal
from app.db.models import LogEntry


router = APIRouter()
logger: structlog.BoundLogger = structlog.get_logger()


@router.get('/admin/logs/query')
async def logs_live(
        level: int = Query(default=logging.INFO, ge=logging.NOTSET, le=logging.CRITICAL),
        event: str = Query(default=None),
        limit: int = Query(default=50, ge=1, le=500),
        offset: int = Query(default=0, ge=0),
):
    stmt = sql.select(LogEntry)

    if level:
        stmt = stmt.where(LogEntry.level >= level)
    if event:
        stmt = stmt.where(LogEntry.event.ilike(f"%{event}%"))

    stmt = stmt\
        .order_by(LogEntry.timestamp.desc()) \
        .offset(offset) \
        .limit(limit)

    async with AsyncSessionLocal() as session:
        return (await session.scalars(stmt)).all()
