# -*- coding=utf-8 -*-
r"""

"""
import json
import asyncio
import logging
import typing as t
import datetime as dt
from functools import cache
from fastapi.encoders import jsonable_encoder
from app.config import SETTINGS


__all__ = ['log_to_db', 'log_processor']


class LogData(t.TypedDict):
    level: int
    module: str
    lineno: int
    message: str
    context: dict
    timestamp: str


fallback_logger = logging.getLogger(__name__)  # fallback logger to keep logging but prevent log-recursion


async def log_to_db(data: LogData):
    from app.db.models import LogEntry
    from app.db.session import AsyncSessionLocal

    try:
        entry = LogEntry(
            level=data['level'],
            module=data['module'],
            lineno=data['lineno'],
            message=data['message'],
            context=data['context'],
            timestamp=dt.datetime.fromisoformat(data['timestamp']),
        )
        # todo: improve somehow with batching
        async with AsyncSessionLocal() as session:
            session.add(entry)
            await session.commit()
    except Exception as e:
        fallback_logger.error("Failed to save log-entry into db", exc_info=e)


async def log_to_redis(data: LogData):
    from app.core.redis import redis_client
    try:
        await redis_client.publish(channel="ws:logs", message=json.dumps({ 'type': "log", 'payload': data }))
    except Exception as e:
        fallback_logger.error("Failed to publish log-entry", exc_info=e)


NAME2LEVEL: dict[str, int] = {
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


EXCLUDE_CONTEXT = {'module', 'lineno', 'event', 'context', 'timestamp', 'level'}


def log_processor(_logger, method: str, event_dict: dict) -> dict:
    level = NAME2LEVEL.get(method, logging.NOTSET)
    if level >= log_to_db_level():
        try:
            data = LogData(
                level=level,
                module=event_dict['module'],
                lineno=event_dict['lineno'],
                message=event_dict['event'],
                context=jsonable_encoder(event_dict, exclude=EXCLUDE_CONTEXT),
                timestamp=event_dict['timestamp'],
            )
            asyncio.create_task(log_to_redis(data))
            asyncio.create_task(log_to_db(data))
        except Exception as e:
            fallback_logger.error("Failed to enqueue log-entry", exc_info=e)

    return event_dict


@cache
def log_to_db_level() -> int:
    return NAME2LEVEL.get(SETTINGS.LOGGING.TO_DB.lower(), logging.NOTSET)
