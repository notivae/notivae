# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, DirectoryPath


__all__ = ["ServerSettings"]


class ServerSettings(BaseSettings):

    STATIC_PATH: str = Field(
        default="/", pattern="^/",
        description="URL basepath for static files",
    )
    STATIC_DIR: DirectoryPath | None = Field(
        default=None,
        description="Path to the static folder",
    )

    model_config = SettingsConfigDict(
        env_prefix="SERVER_",
        env_ignore_empty=True,
    )
