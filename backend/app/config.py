# -*- coding=utf-8 -*-
r"""

"""
from pydantic_settings import BaseSettings


__all__ = ['settings']


class BackendSettings(BaseSettings):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8765

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = BackendSettings()
