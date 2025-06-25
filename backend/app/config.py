# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError, IPvAnyAddress, AnyUrl


__all__ = ['settings']


class BackendSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        description="shows additional information in some parts of the app",
    )

    LOGGING_LEVEL: t.Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO',
        description="Minimum severity of messages to log",
    )
    LOGGING_FORMAT: t.Literal['console', 'json'] = Field(
        default='console',
        description="Output format for logs: human-readable ('console') or structured ('json')",
    )
    LOG_TO_DB: bool = Field(
        default=True,
        description="If true, logs will also be persisted to the database",
    )

    APP_HOST: IPvAnyAddress = Field(
        default='0.0.0.0',
        description="IP address to bind the server to (e.g., 0.0.0.0 for all interfaces)",
    )
    APP_PORT: int = Field(
        default=8765, gt=0, lt=65535,
        description="Port number for the application server",
    )

    DATABASE_URL: AnyUrl = Field(
        default=...,
        description="Full database connection URL (e.g., postgresql+asyncpg://user:pass@host:port/dbname)",
    )
    DATABASE_POOL_SIZE: int = Field(
        default=5, ge=0,
        description="Number of persistent database connections per worker",
    )
    DATABASE_POOL_MAX_OVERFLOW: int = Field(
        default=10, ge=0,
        description="Additional temporary connections allowed when the pool is full",
    )
    DATABASE_POOL_TIMEOUT: int = Field(
        default=30, ge=0,
        description="Time (in seconds) to wait for a connection before raising an error",
    )
    DATABASE_POOL_RECYCLE: int = Field(
        default=1800, ge=0,
        description="Time (in seconds) after which idle DB connections will be recycled",
    )

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env", env_file_charset="utf-8", env_ignore_empty=True,
    )


try:
    settings = BackendSettings()
except ValidationError as e:
    import sys
    print(e, file=sys.stderr)
    sys.exit(1)
