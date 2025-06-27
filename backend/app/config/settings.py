# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from .app import AppSettings
from .database import DatabaseSettings
from .gzip import GzipSettings
from .logging import LoggingSettings


__all__ = ['BackendSettings']


class BackendSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        description="shows additional information in some parts of the app",
    )

    APP: AppSettings = Field(default_factory=AppSettings)
    DATABASE: DatabaseSettings = Field(default_factory=DatabaseSettings)
    GZIP: GzipSettings = Field(default_factory=GzipSettings)
    LOGGING: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
    )
