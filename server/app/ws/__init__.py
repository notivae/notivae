# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, WebSocket


router = APIRouter()


@router.websocket(path='/api/ws')
async def websocket_endpoint(
        websocket: WebSocket,
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Data: {data}")
