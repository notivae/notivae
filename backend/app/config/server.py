# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, IPvAnyAddress, DirectoryPath


__all__ = ["ServerSettings"]


class ServerSettings(BaseSettings):

    HOST: IPvAnyAddress = Field(
        default='0.0.0.0',
        description="IP address to bind the server to (e.g., 0.0.0.0 for all interfaces)",
    )
    PORT: int = Field(
        default=8765, gt=0, lt=65535,
        description="Port number for the application server",
    )

    STATIC_PATH: str = Field(
        default="/", pattern="^/",
        description="URL basepath for static files",
    )
    STATIC_DIR: t.Optional[DirectoryPath] = Field(
        default=None,
        description="Path to the static folder",
    )

    model_config = SettingsConfigDict(
        env_prefix="SERVER_",
        env_ignore_empty=True,
    )
