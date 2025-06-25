# -*- coding=utf-8 -*-
r"""

"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from ..config import settings


engine = create_async_engine(
    url=str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    poolclass=AsyncAdaptedQueuePool,
)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
