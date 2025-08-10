# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["SecuritySettings"]


class SecuritySettings(BaseSettings):

    SECRET_KEY: str = Field(
        default=..., min_length=32,
        description="Secret key to use for security tokens. `openssl rand -hex 32`"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
    )

    TRUST_PROXY_HEADERS: bool = Field(
        default=False,
        description="Enable this if you are behind a proxy. The server used header to extract the client-ip for identification",
    )

    SESSION_TOKEN_NBYTES: int = Field(
        default=32, ge=8,
        description="The number of bytes to use for session identification",
    )

    DISABLE_RATE_LIMITS: bool = Field(
        default=False,
        description="Whether to disable rate limiting. (recommended only for development)",
    )

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        env_ignore_empty=True,
    )
