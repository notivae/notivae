# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .callback import router as callback_router
from .register import router as register_router
from .request import router as request_router
from .unlink import router as unlink_router

router = APIRouter(prefix='/magic', tags=['Magic Link'])
router.include_router(callback_router)
router.include_router(register_router)
router.include_router(request_router)
router.include_router(unlink_router)
