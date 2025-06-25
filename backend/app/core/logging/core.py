# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import logging
from app.db.session import AsyncSessionLocal
from app.db.models import LogEntry


__all__ = ['log_queue', 'log_subscribers', 'db_log_worker', 'log_db_processor']


log_queue = asyncio.Queue()
log_subscribers: set[asyncio.Queue] = set()


fallback_logger = logging.getLogger(__name__)


async def db_log_worker():
    print("db-log-worker started")
    while True:
        log_item: LogEntry = await log_queue.get()
        print("db_log_worker", [log_item])
        try:
            async with AsyncSessionLocal() as session:
                session.add(log_item)
                await session.commit()
        except Exception as e:
            fallback_logger.error("Failed to save log-entry", exc_info=e)
        for subscriber in list(log_subscribers):
            try:
                subscriber.put_nowait(log_item)
            except asyncio.QueueFull:
                pass


NAME2LEVEL: dict[str, int] = {
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


def log_db_processor(logger, method: str, event_dict: dict) -> dict:
    print("log_db_processor", [logger, method, event_dict])
    try:
        level = NAME2LEVEL.get(method, logging.INFO)
        entry = LogEntry(
            level=level,
            event=event_dict.get('event', "<no-event>"),
            message=event_dict.get('message', "<no-message>"),
            context={ k: v for k, v in event_dict.items() if k not in {'event', 'message', 'context', 'timestamp', 'level'}},
        )
        asyncio.create_task(log_queue.put(entry))
    except Exception as e:
        fallback_logger.error("Failed to enqueue log-entry", exc_info=e)

    return event_dict
