# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["AuthLocalSettings"]


class AuthLocalSettings(BaseSettings):
    ENABLED: bool = Field(
        default=True,
        description="Whether to enable password based authentication.",
    )

    model_config = SettingsConfigDict(
        env_prefix="AUTH_LOCAL_",
        env_ignore_empty=True,
    )
