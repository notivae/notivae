# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import redis.asyncio as redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from app.config import SETTINGS


__all__ = ['redis_client', 'PubSubMessage']


redis_client = redis.from_url(
    url=str(SETTINGS.REDIS.URL),
    decode_responses=True,
    retry=Retry(
        retries=SETTINGS.REDIS.RETRIES,
        backoff=ExponentialBackoff(),
    ),
)


class PubSubMessage(t.TypedDict):
    type: str
    pattern: t.Optional[str]
    channel: t.Optional[str]
    data: t.Any
