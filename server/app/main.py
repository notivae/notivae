# -*- coding=utf-8 -*-
r"""

"""
from app.config import SETTINGS
from app.core.logging import setup_logging; setup_logging(settings=SETTINGS.LOGGING)
import typing as t
import fastapi
from fastapi.middleware.gzip import GZipMiddleware
import pydantic
from app.lifespan import lifespan
from fastapi.staticfiles import StaticFiles

from app.api import router as api_router


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
app.add_middleware(
    GZipMiddleware,
    minimum_size=SETTINGS.GZIP.MINIMUM_SIZE,
    compresslevel=SETTINGS.GZIP.LEVEL,
)
app.include_router(api_router)


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
