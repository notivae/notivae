# -*- coding=utf-8 -*-
r"""

"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from ..config import SETTINGS


engine = create_async_engine(
    url=str(SETTINGS.DATABASE.URL),
    echo=SETTINGS.DEBUG,
    pool_size=SETTINGS.DATABASE.POOL_SIZE,
    max_overflow=SETTINGS.DATABASE.POOL_MAX_OVERFLOW,
    pool_timeout=SETTINGS.DATABASE.POOL_TIMEOUT,
    pool_recycle=SETTINGS.DATABASE.POOL_RECYCLE,
    poolclass=AsyncAdaptedQueuePool,
)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
