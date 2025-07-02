# -*- coding=utf-8 -*-
r"""

"""
import structlog
from app.config.logging import LoggingSettings
from .core import log_db_processor


def setup_logging(settings: LoggingSettings):
    processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.TO_DB:
        processors.append(log_db_processor)

    if settings.FORMAT == 'json':
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(min_level=settings.LEVEL.lower()),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
