# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, Depends
from app.core.dependencies import require_system_admin
from .logs import router as logs_router
from .notifications import router as notifications_router


router = APIRouter(prefix="/admin", dependencies=[Depends(require_system_admin)])
router.include_router(logs_router)
router.include_router(notifications_router)
