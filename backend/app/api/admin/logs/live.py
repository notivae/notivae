# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import structlog
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from app.core.logging import log_subscribers
from app.core.util import get_client_ip

router = APIRouter()
logger: structlog.BoundLogger = structlog.get_logger()


@router.get('/admin/logs/live')
async def logs_live(request: Request):
    # todo: add authentication
    logger.info("logs_live", message="new listener connected", client=get_client_ip(request=request))

    queue = asyncio.Queue(maxsize=100)
    log_subscribers.add(queue)

    async def event_stream():
        try:
            while not await request.is_disconnected():
                event = await queue.get()
                yield f"data: {jsonable_encoder(event)}\n\n"
        finally:
            log_subscribers.discard(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
