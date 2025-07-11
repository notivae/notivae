# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .clamav import router as clamav_router
from .mail import router as mail_router


router = APIRouter(prefix="/dev", tags=["dev"])
router.include_router(clamav_router)
router.include_router(mail_router)
