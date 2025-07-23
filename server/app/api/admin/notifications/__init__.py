# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .broadcast import router as broadcast_router


router = APIRouter(prefix="/notifications", tags=["Notifications"])
router.include_router(broadcast_router)
