# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, IPvAnyAddress


__all__ = ["AppSettings"]


class AppSettings(BaseSettings):

    HOST: IPvAnyAddress = Field(
        default='0.0.0.0',
        description="IP address to bind the server to (e.g., 0.0.0.0 for all interfaces)",
    )
    PORT: int = Field(
        default=8765, gt=0, lt=65535,
        description="Port number for the application server",
    )


    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_ignore_empty=True,
    )
