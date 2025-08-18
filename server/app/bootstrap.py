# -*- coding=utf-8 -*-
r"""

"""
from app.config import SETTINGS
from app.core.logging import setup_logging

setup_logging(settings=SETTINGS.LOGGING)

import mimetypes
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('video/webm', ".webm")
