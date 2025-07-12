# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["MagicLinkSettings"]


class MagicLinkSettings(BaseSettings):
    ENABLED: bool = Field(
        default=True,
        description="Whether to enable magic-link authentication.",
    )

    model_config = SettingsConfigDict(
        env_prefix="MAGIC_LINK_",
        env_ignore_empty=True,
    )
