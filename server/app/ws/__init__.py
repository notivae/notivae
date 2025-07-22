# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import asyncio
import structlog
from fastapi import APIRouter, WebSocket, WebSocketException, status, WebSocketDisconnect, Cookie
import sqlalchemy as sql
from app.core.redis import redis_client, PubSubMessage
from app.db.session import AsyncSessionLocal
from app.db.models import AuthSession
from app.core.security.auth_session import hash_session_token


router = APIRouter()
logger = structlog.get_logger()


@router.websocket(path='/api/ws')
async def websocket_endpoint(
        websocket: WebSocket,
        session_token: t.Optional[str] = Cookie(default=None),
):
    logger.info(f"websocket connection opened")

    await websocket.accept()

    if session_token is None:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing session token",
        )

    session_token_hashed = hash_session_token(session_token)

    # not via `Depends` as the dependency would keep the db-connection open for longer than needed
    async with AsyncSessionLocal() as session:
        stmt = sql.select(AuthSession).where(AuthSession.hashed_token == session_token_hashed)
        auth_session: AuthSession = await session.scalar(stmt)
        if not AuthSession.is_valid(auth_session):
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid session token",
            )

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
        raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason="critical error")


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
