# -*- coding=utf-8 -*-
r"""

"""
import redis.asyncio as redis
from app.config import SETTINGS


__all__ = ['redis_client']


redis_client = redis.from_url(SETTINGS.REDIS.URL)
