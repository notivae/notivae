# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, EmailStr, NameEmail, DirectoryPath


__all__ = ["MailSettings"]


class MailSettings(BaseSettings):

    SERVER: str = Field(
        default=...,
        description="Server name (or IP) to connect to",
    )
    PORT: int = Field(
        default=None, gt=0,
        description="Server port. defaults 465 if use_tls is True, 587 if start_tls is True, or 25 otherwise",
    )

    USE_CREDENTIALS: bool = Field(
        default=True,
        description="Whether or not to use credentials when connecting to server",
    )
    USERNAME: str = Field(
        default=...,
        description="Username to login as after connect",
    )
    PASSWORD: SecretStr = Field(
        default=...,
        description="Password for login after connect",
    )

    FROM: t.Union[EmailStr, NameEmail] = Field(
        default=...,
    )

    USE_TLS: bool = Field(
        default=False,
        description="If True, make the initial connection to the server over TLS/SSL. Mutually exclusive with start_tls; if the server uses STARTTLS, use_tls should be False",
    )
    START_TLS: bool = Field(
        default=None,
        description="Flag to initiate a STARTTLS upgrade on connect. If None (the default), upgrade will be initiated if supported by the server. If True, and upgrade will be initiated regardless of server support. If False, no upgrade will occur. Mutually exclusive with use_tls",
    )

    VALIDATE_CERTS: bool = Field(
        default=True,
        description="Determines if server certificates are validated",
    )

    TEMPLATES_DIR: t.Optional[DirectoryPath] = Field(
        default=None,
        description="[Override] Directory where mail-templates are located",
    )

    model_config = SettingsConfigDict(
        env_prefix="MAIL_",
        env_ignore_empty=True,
    )
