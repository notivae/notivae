# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .admin import router as admin_router


router = APIRouter(prefix="/api")
router.include_router(admin_router)
