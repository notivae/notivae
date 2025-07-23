# -*- coding=utf-8 -*-
r"""

"""
from app.config import SETTINGS
from app.core.logging import setup_logging

setup_logging(settings=SETTINGS.LOGGING)
