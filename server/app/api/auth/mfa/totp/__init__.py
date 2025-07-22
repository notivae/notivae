# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .confirm import router as confirm_router
from .init import router as enable_router
from .remove import router as remove_router
from .verify import router as verify_router


router = APIRouter(prefix='/totp', tags=['MFA TOTP'])
router.include_router(confirm_router)
router.include_router(enable_router)
router.include_router(remove_router)
router.include_router(verify_router)
