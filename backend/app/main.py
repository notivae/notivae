# -*- coding=utf-8 -*-
r"""

"""
from app.core.logging import setup_logging; setup_logging()
import typing as t
import fastapi
import pydantic
from app.config import settings
from app.lifespan import lifespan

from app.api import router as api_router


app = fastapi.FastAPI(
    debug=True,
    title="Notivae",
    version="0.0.0",
    lifespan=lifespan,
)
app.include_router(api_router)


class HealthResponse(pydantic.BaseModel):
    status: t.Literal["ok"]

@app.get("/health", response_model=HealthResponse)
def health():
    return { 'status': "ok" }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)
