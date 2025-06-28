# -*- coding=utf-8 -*-
r"""

"""
from pydantic import ValidationError
from ._settings import BackendSettings


__all__ = ['SETTINGS']


try:
    SETTINGS = BackendSettings()
    if SETTINGS.DEBUG:
        print(SETTINGS)
except ValidationError as e:
    import sys
    print(e, file=sys.stderr)
    sys.exit(1)
