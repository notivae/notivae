# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .regenerate import router as regenerate_router
from .verify import router as verify_router


router = APIRouter(prefix='/backup', tags=['MFA Backup Codes'])
router.include_router(regenerate_router)
router.include_router(verify_router)
