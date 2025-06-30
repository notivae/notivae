# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .admin import router as admin_router
from .auth import router as auth_router
from .users import router as users_router


router = APIRouter(prefix="/api")
router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(users_router)
