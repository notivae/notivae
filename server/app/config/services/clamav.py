# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["ClamAVSettings"]


class ClamAVSettings(BaseSettings):

    SERVER: str = Field(
        default=...,
        description="Server name (or IP) to connect to",
    )
    PORT: int = Field(
        default=3310, gt=0,
        description="Server port",
    )

    model_config = SettingsConfigDict(
        env_prefix="CLAMAV_",
        env_ignore_empty=True,
    )
