# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from ._utils import make_optional_factory
from .app import AppSettings
from .assets import AssetsSettings
from .database import DatabaseSettings
from .gzip import GzipSettings
from .logging import LoggingSettings
from .redis import RedisSettings
from .security import SecuritySettings
from .server import ServerSettings

from .services.mail import MailSettings
from .services.clamav import ClamAVSettings

from .auth.discord import DiscordSettings
from .auth.local import AuthLocalSettings
from .auth.oidc import OidcSettings
from .auth.magic_link import MagicLinkSettings


__all__ = ['BackendSettings']


class BackendSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        description="shows additional information in some parts of the app",
    )

    APP: AppSettings = Field(default_factory=AppSettings)
    ASSETS: AssetsSettings = Field(default_factory=AssetsSettings)
    SERVER: ServerSettings = Field(default_factory=ServerSettings)
    SECURITY: SecuritySettings = Field(default_factory=SecuritySettings)
    DATABASE: DatabaseSettings = Field(default_factory=DatabaseSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)
    GZIP: GzipSettings = Field(default_factory=GzipSettings)
    LOGGING: LoggingSettings = Field(default_factory=LoggingSettings)

    MAIL: None | MailSettings = Field(default_factory=make_optional_factory(MailSettings))
    CLAMAV: None | ClamAVSettings = Field(default_factory=make_optional_factory(ClamAVSettings))

    AUTH_LOCAL: None | AuthLocalSettings = Field(default_factory=make_optional_factory(AuthLocalSettings))
    MAGIC_LINK: None | MagicLinkSettings = Field(default_factory=make_optional_factory(MagicLinkSettings))
    DISCORD: None | DiscordSettings = Field(default_factory=make_optional_factory(DiscordSettings))
    OIDC: None | OidcSettings = Field(default_factory=make_optional_factory(OidcSettings))

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
    )
