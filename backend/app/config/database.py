# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl, model_validator


__all__ = ["DatabaseSettings"]


class DatabaseSettings(BaseSettings):

    URL: AnyUrl = Field(
        default=...,
        description="Full database connection URL (e.g., postgresql+asyncpg://user:pass@host:port/dbname)",
    )
    POOL_SIZE: int = Field(
        default=5, ge=0,
        description="Number of persistent database connections per worker",
    )
    POOL_MAX_OVERFLOW: int = Field(
        default=10, ge=0,
        description="Additional temporary connections allowed when the pool is full",
    )
    POOL_TIMEOUT: int = Field(
        default=30, ge=0,
        description="Time (in seconds) to wait for a connection before raising an error",
    )
    POOL_RECYCLE: int = Field(
        default=1800, ge=0,
        description="Time (in seconds) after which idle DB connections will be recycled",
    )

    @model_validator(mode='before')
    @classmethod
    def build_url_from_parts(cls, data: dict) -> dict:
        import os

        if not data.get('URL'):
            user = os.getenv('POSTGRES_USER')
            password = os.getenv('POSTGRES_PASSWORD')
            db = os.getenv('POSTGRES_DB')
            host = os.getenv('POSTGRES_HOST', 'localhost')
            port = os.getenv('POSTGRES_PORT', '5432')

            if all([user, password, db, host, port]):
                data['URL'] = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        return data

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_ignore_empty=True,
    )
