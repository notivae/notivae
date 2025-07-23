# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from ._enums import AccountCreationMode


__all__ = ["AppSettings"]


class AppSettings(BaseSettings):

    ACCOUNT_CREATION: AccountCreationMode = Field(
        default=AccountCreationMode.RESTRICTED,
        description="account creation mode",
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_ignore_empty=True,
    )
