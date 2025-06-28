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

from app.api import router as api_router


app = fastapi.FastAPI(
    debug=True,
    title="Notivae",
    version="0.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    GZipMiddleware,
    minimum_size=SETTINGS.GZIP.MINIMUM_SIZE,
    compresslevel=SETTINGS.GZIP.LEVEL,
)
app.include_router(api_router)


class HealthResponse(pydantic.BaseModel):
    status: t.Literal["ok"]

@app.get("/health", response_model=HealthResponse)
def health():
    return { 'status': "ok" }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host=SETTINGS.SERVER.HOST, port=SETTINGS.SERVER.PORT)
