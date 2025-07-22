# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .backup import router as backup_router
from .totp import router as totp_router


router = APIRouter(prefix="/mfa", tags=["MFA"])
router.include_router(backup_router)
router.include_router(totp_router)
