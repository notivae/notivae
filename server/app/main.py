# -*- coding=utf-8 -*-
r"""

"""
from app import bootstrap  # noqa: F401

import typing as t
import pydantic
import fastapi
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import SETTINGS
from app.lifespan import lifespan
from app.exception_handlers import register_exception_handlers

from app.api import router as api_router
from app.ws import router as ws_router


app = fastapi.FastAPI(
    debug=True,
    title="Notivae",
    version="0.0.0",
    lifespan=lifespan,
    contact=dict(
        name="notivae",
        url="https://github.com/notivae/notivae",
    ),
    license_info=dict(
        name="GNU GENERAL PUBLIC LICENSE 3.0",
        identifier="GPL-3.0-or-later"
    )
)
register_exception_handlers(app=app)
app.add_middleware(
    GZipMiddleware,
    minimum_size=SETTINGS.GZIP.MINIMUM_SIZE,
    compresslevel=SETTINGS.GZIP.LEVEL,
)
app.include_router(api_router)
app.include_router(ws_router)


class HealthResponse(pydantic.BaseModel):
    status: t.Literal["ok"]

@app.get("/healthz", response_model=HealthResponse)
def health():
    return { 'status': "ok" }


if SETTINGS.SERVER.STATIC_PATH and SETTINGS.SERVER.STATIC_DIR:
    app.mount(
        path=SETTINGS.SERVER.STATIC_PATH,
        app=StaticFiles(
            directory=SETTINGS.SERVER.STATIC_DIR,
            html=True,
        ),
        name="static",
    )
