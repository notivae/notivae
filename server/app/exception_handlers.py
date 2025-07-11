# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from app.services.virus_scanning.lib import ClamAVConnectionError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ClamAVConnectionError)
    async def clam_av_connection_exception_handler(_request: Request, _exc: ClamAVConnectionError):
        return JSONResponse(
            content={'detail': "ClamAV is currently unavailable"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
