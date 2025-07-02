# -*- coding=utf-8 -*-
r"""

"""
import json
import asyncio
import logging
from fastapi.encoders import jsonable_encoder
from app.db.session import AsyncSessionLocal
from app.db.models import LogEntry
from app.core.redis import redis_client
from app.config import SETTINGS


__all__ = ['REDIS_CHANNEL', 'log_to_db', 'log_db_processor']


REDIS_CHANNEL = "logs"


fallback_logger = logging.getLogger(__name__)  # fallback logger to keep logging but prevent log-recursion


async def log_to_db(entry: LogEntry):
    try:
        # todo: improve somehow with batching
        async with AsyncSessionLocal() as session:
            session.add(entry)
            await session.commit()
    except Exception as e:
        fallback_logger.error("Failed to save log-entry into db", exc_info=e)


async def log_to_redis(entry: LogEntry):
    try:
        await redis_client.publish(channel=REDIS_CHANNEL, message=json.dumps(jsonable_encoder(entry)))
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


def log_db_processor(_logger, method: str, event_dict: dict) -> dict:
    try:
        level = NAME2LEVEL.get(method, logging.INFO)
        entry = LogEntry(
            level=level,
            event=event_dict['event'],
            message=event_dict.get('message', None),
            context={ k: v for k, v in event_dict.items() if k not in {'event', 'message', 'context', 'timestamp', 'level'}},
        )
        if SETTINGS.LOGGING.TO_DB:
            asyncio.create_task(log_to_db(entry))
        asyncio.create_task(log_to_redis(entry))
    except Exception as e:
        fallback_logger.error("Failed to enqueue log-entry", exc_info=e)

    return event_dict
