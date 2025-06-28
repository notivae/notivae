# -*- coding=utf-8 -*-
r"""

"""
from app.db.session import AsyncSessionLocal


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
