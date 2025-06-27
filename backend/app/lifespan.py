# -*- coding=utf-8 -*-
r"""

"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import SETTINGS
from app.core.logging.core import db_log_worker

__all__ = ['lifespan']


@asynccontextmanager
async def lifespan(app: FastAPI):
    if SETTINGS.LOGGING.TO_DB:
        asyncio.create_task(db_log_worker())

    yield  ## app running

    ## shutdown
