# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.services.virus_scanning import SUPPORTED, scan_abuffer


router = APIRouter(prefix="/clamav")


class ClamAVTestResponse(BaseModel):
    save: bool
    detail: t.Optional[str]


@router.post("/test", response_model=ClamAVTestResponse)
async def post_mail_test(
        file: UploadFile = File(...),
):
    if not SUPPORTED:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="ClamAV service is not supported")

    result = await scan_abuffer(buffer=file)

    return ClamAVTestResponse(save=result.save, detail=result.virus_name)
