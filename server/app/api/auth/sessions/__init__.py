# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .get import router as get_router
from .revoke import router as revoke_router


router = APIRouter(prefix="/sessions", tags=["Sessions"])
router.include_router(get_router)
router.include_router(revoke_router)
