# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Depends
from .logs import router as logs_router
from app.core.dependencies import require_system_admin


router = APIRouter(prefix="/admin", dependencies=[Depends(require_system_admin)])
router.include_router(logs_router)
