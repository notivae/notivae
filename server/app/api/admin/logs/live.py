# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import structlog
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.core.logging import REDIS_CHANNEL
from app.core.util import get_client_ip
from app.core.redis import redis_client


router = APIRouter()
logger: structlog.BoundLogger = structlog.get_logger()


@router.get('/live', response_class=StreamingResponse)
async def logs_live(
        request: Request,
):
    logger.info("new listener connected", client=get_client_ip(request=request))

    return EventSourceResponse(event_stream(request=request), media_type="text/event-stream")


async def event_stream(request: Request):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL)

    try:
        while not await request.is_disconnected():
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if message:
                log_entry_json = message['data']
                yield ServerSentEvent(
                    data=log_entry_json,
                )
            await asyncio.sleep(0.01)
    finally:
        await pubsub.unsubscribe(REDIS_CHANNEL)
        await pubsub.aclose()
