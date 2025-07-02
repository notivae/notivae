# -*- coding=utf-8 -*-
r"""

"""
from contextlib import asynccontextmanager
from fastapi import FastAPI


__all__ = ['lifespan']


@asynccontextmanager
async def lifespan(app: FastAPI):
    ## startup

    yield  ## app running

    ## shutdown
