# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from app.config import SETTINGS
from .logout import router as logout_router


router = APIRouter(prefix='/auth', tags=['Auth'])
router.include_router(logout_router)

if SETTINGS.OIDC:
    from .oidc import router as oidc_router
    router.include_router(oidc_router)
