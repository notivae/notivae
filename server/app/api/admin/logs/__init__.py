# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .live import router as live_router
from .query import router as query_router


router = APIRouter(prefix="/logs", tags=["logs"])
router.include_router(live_router)
router.include_router(query_router)
