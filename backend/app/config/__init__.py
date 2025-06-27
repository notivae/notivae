# -*- coding=utf-8 -*-
r"""

"""
from pydantic import ValidationError
from .settings import BackendSettings


__all__ = ['SETTINGS']


try:
    SETTINGS = BackendSettings()
except ValidationError as e:
    import sys
    print(e, file=sys.stderr)
    sys.exit(1)
