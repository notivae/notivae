# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .get import router as get_router


router = APIRouter(prefix="/logs", tags=["logs"])
router.include_router(get_router)
