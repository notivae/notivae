# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from app.config import SETTINGS
from .admin import router as admin_router
from .auth import router as auth_router
from .features import router as features_router
from .security import router as security_router
from .user import router as user_router


router = APIRouter(prefix="/api")
router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(features_router)
router.include_router(security_router)
router.include_router(user_router)

if SETTINGS.DEBUG:
    from .dev import router as dev_router
    router.include_router(dev_router)
