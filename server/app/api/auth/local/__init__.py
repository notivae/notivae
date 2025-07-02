# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .login import router as login_router
from .register import router as register_router
from .unlink import router as unlink_router

router = APIRouter(prefix='/local', tags=['Auth Local'])
router.include_router(login_router)
router.include_router(register_router)
router.include_router(unlink_router)
