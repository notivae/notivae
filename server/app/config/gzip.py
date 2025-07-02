# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["GzipSettings"]


class GzipSettings(BaseSettings):
    MINIMUM_SIZE: int = Field(
        default=1_000, ge=0,
        description="Minimum payload size in bytes required to enable gzip compression. Payloads below this threshold will be sent uncompressed",
    )
    LEVEL: int = Field(
        default=6, ge=1, le=9,
        description="Compression strength for gzip. 1 = fastest, least compression. 9 = slowest, best compression. 6 is a good balance for most use cases",
    )

    model_config = SettingsConfigDict(
        env_prefix="GZIP_",
        env_ignore_empty=True,
    )
