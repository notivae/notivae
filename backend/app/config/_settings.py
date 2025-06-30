# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from ._utils import make_optional_factory
from .app import AppSettings
from .database import DatabaseSettings
from .gzip import GzipSettings
from .logging import LoggingSettings
from .redis import RedisSettings
from .security import SecuritySettings
from .server import ServerSettings

from .discord import DiscordSettings
from .oidc import OidcSettings


__all__ = ['BackendSettings']


class BackendSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        description="shows additional information in some parts of the app",
    )

    APP: AppSettings = Field(default_factory=AppSettings)
    SERVER: ServerSettings = Field(default_factory=ServerSettings)
    SECURITY: SecuritySettings = Field(default_factory=SecuritySettings)
    DATABASE: DatabaseSettings = Field(default_factory=DatabaseSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)
    GZIP: GzipSettings = Field(default_factory=GzipSettings)
    LOGGING: LoggingSettings = Field(default_factory=LoggingSettings)

    DISCORD: t.Optional[DiscordSettings] = Field(default_factory=make_optional_factory(DiscordSettings))
    OIDC: t.Optional[OidcSettings] = Field(default_factory=make_optional_factory(OidcSettings))

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
    )
