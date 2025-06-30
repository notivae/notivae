# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl


__all__ = ["RedisSettings"]


class RedisSettings(BaseSettings):

    URL: AnyUrl = Field(
        default=...,
        description="Full redis connection URL (e.g., redis://localhost:6379)",
    )

    RETRIES: int = Field(
        default=3, ge=1,
        description="Number of times to retry connecting to Redis",
    )

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_ignore_empty=True,
    )
