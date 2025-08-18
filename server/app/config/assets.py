# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, DirectoryPath


__all__ = ['AssetsSettings']


class AssetsSettings(BaseSettings):

    STORAGE_ROOT: DirectoryPath = Field(
        default="/storage",
        description="The root path where assets should be stored."
    )

    MAXIMUM_SIZE_BYTES: int = Field(
        default=25 * 1024 * 1024, ge=0,
        description="The maximum file size in bytes. Set to 0 to disable maximum size."
    )

    model_config = SettingsConfigDict(
        env_prefix="ASSETS_",
        env_ignore_empty=True,
    )
