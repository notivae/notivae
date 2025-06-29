# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from ._utils import make_optional_factory
from .server import ServerSettings
from .database import DatabaseSettings
from .gzip import GzipSettings
from .logging import LoggingSettings
from .oidc import OidcSettings
from .redis import RedisSettings


__all__ = ['BackendSettings']


class BackendSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        description="shows additional information in some parts of the app",
    )

    SERVER: ServerSettings = Field(default_factory=ServerSettings)
    DATABASE: DatabaseSettings = Field(default_factory=DatabaseSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)
    GZIP: GzipSettings = Field(default_factory=GzipSettings)
    LOGGING: LoggingSettings = Field(default_factory=LoggingSettings)

    OIDC: t.Optional[OidcSettings] = Field(default_factory=make_optional_factory(OidcSettings))

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
    )
