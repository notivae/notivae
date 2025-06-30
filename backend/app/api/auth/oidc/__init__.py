# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .callback import router as callback_router
from .redirect import router as redirect_router
from .unlink import router as unlink_router

router = APIRouter(prefix='/oidc', tags=['OIDC'])
router.include_router(callback_router)
router.include_router(redirect_router)
router.include_router(unlink_router)
