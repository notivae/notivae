# -*- coding=utf-8 -*-
r"""

"""
import json
import asyncio
import logging
import typing as t
from fastapi.encoders import jsonable_encoder
from app.db.session import AsyncSessionLocal
from app.db.models import LogEntry
from app.core.redis import redis_client
from app.config import SETTINGS


__all__ = ['REDIS_CHANNEL', 'log_to_db', 'log_processor']


REDIS_CHANNEL = "logs"


class LogData(t.TypedDict):
    level: int
    module: str
    lineno: int
    message: str
    context: dict


fallback_logger = logging.getLogger(__name__)  # fallback logger to keep logging but prevent log-recursion


async def log_to_db(data: LogData):
    try:
        entry = LogEntry(**data)
        # todo: improve somehow with batching
        async with AsyncSessionLocal() as session:
            session.add(entry)
            await session.commit()
    except Exception as e:
        fallback_logger.error("Failed to save log-entry into db", exc_info=e)


async def log_to_redis(data: LogData):
    try:
        await redis_client.publish(channel=REDIS_CHANNEL, message=json.dumps(data))
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
    try:
        level = NAME2LEVEL.get(method, logging.NOTSET)
        data = LogData(
            level=level,
            module=event_dict['module'],
            lineno=event_dict['lineno'],
            message=event_dict['event'],
            context=jsonable_encoder(event_dict, exclude=EXCLUDE_CONTEXT),
        )
        if SETTINGS.LOGGING.TO_DB:
            asyncio.create_task(log_to_db(data))
        asyncio.create_task(log_to_redis(data))
    except Exception as e:
        fallback_logger.error("Failed to enqueue log-entry", exc_info=e)

    return event_dict
