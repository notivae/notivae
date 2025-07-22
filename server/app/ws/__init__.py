# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import structlog
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect
from app.core.redis import redis_client, PubSubMessage


router = APIRouter()
logger = structlog.get_logger()


@router.websocket(path='/api/ws')
async def websocket_endpoint(
        websocket: WebSocket,
):
    logger.info(f"websocket connection opened")
    await websocket.accept()

    # todo: authenticate
    if False:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication")
        return

    listener = asyncio.create_task(websocket_listener(websocket=websocket))
    sender = asyncio.create_task(websocket_sender(websocket=websocket))

    done, pending = await asyncio.wait(
        [listener, sender],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    if any(f.exception() for f in done):
        for task in done:
            exc = task.exception()
            if exc:
                logger.error(f"websocket closed unexpectedly ({type(exc)}: {exc})", exc_info=exc)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="critical error")
    else:
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE, reason="WebSocket lifecycle end")


async def websocket_listener(websocket: WebSocket):
    try:
        while True:
            data = await websocket.receive_text()  # todo: validate against pydantic classes
            await redis_client.publish(f"ws:data", data)  # todo: adjust channel
    except WebSocketDisconnect:
        pass


async def websocket_sender(websocket: WebSocket):
    try:
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("ws:data")
        while True:
            message: PubSubMessage = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10)
            if message is None:
                await websocket.send_json({ 'type': 'keepalive' })
            else:
                await websocket.send_text(message['data'])
    except WebSocketDisconnect:
        pass
