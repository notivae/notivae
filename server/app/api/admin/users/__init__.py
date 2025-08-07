# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .list import router as list_router


router = APIRouter(prefix="/users", tags=["User Management"])
router.include_router(list_router)
