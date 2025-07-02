# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl


__all__ = ["DiscordSettings"]


class DiscordSettings(BaseSettings):
    CLIENT_ID: str = Field(
        default=...,
        description="Client ID issued by the OpenID Connect provider",
    )
    CLIENT_SECRET: str = Field(
        default=...,
        description="Client secret associated with the OpenID Connect client",
    )

    DISCOVERY_URI: HttpUrl = Field(
        default="https://discord.com/.well-known/openid-configuration",
        description="OpenID Configuration endpoint URI for discord",
    )

    SCOPES: str = Field(
        default="identity email",
        description="Scopes requested from the OpenID Connect provider during authentication",
    )

    model_config = SettingsConfigDict(
        env_prefix="DISCORD_",
        env_ignore_empty=True,
    )
