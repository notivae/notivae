# -*- coding=utf-8 -*-
r"""

"""
import os
import typing as t
from pydantic_settings import BaseSettings


__all__ = ['make_optional_factory']


def make_optional_factory(cls: t.Type['BaseSettings']):
    r"""
    converts a pydantic-settings model to an optional factory that only instantiates if at least on field is defined
    via environment variables.
    :param cls: class to convert
    :return: factory for `cls`
    """

    options = { k for k in cls.__annotations__.keys() if k.isupper() }
    prefix = cls.model_config['env_prefix']
    env_keys = { f"{prefix}{opt}" for opt in options }

    def factory():
        any_key_defined = any(os.getenv(k) for k in env_keys)
        return cls() if any_key_defined else None

    return factory
