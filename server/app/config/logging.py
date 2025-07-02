# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


__all__ = ["LoggingSettings"]


class LoggingSettings(BaseSettings):

    LEVEL: t.Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO',
        description="Minimum severity of messages to log",
    )

    FORMAT: t.Literal['console', 'json'] = Field(
        default='console',
        description="Output format for logs: human-readable ('console') or structured ('json')",
    )

    TO_DB: bool = Field(
        default=True,
        description="If true, logs will also be persisted to the database",
    )


    model_config = SettingsConfigDict(
        env_prefix="LOGGING_",
        env_ignore_empty=True,
    )
