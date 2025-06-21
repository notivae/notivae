# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import fastapi
import pydantic
from app.config import settings


app = fastapi.FastAPI(
    debug=True,
    title="Notivae",
    version="0.0.0",
)


class HealthResponse(pydantic.BaseModel):
    status: t.Literal["ok"]

@app.get("/health", response_model=HealthResponse)
def health():
    return { 'status': "ok" }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)
