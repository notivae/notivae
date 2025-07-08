# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .approve_account import router as approve_account_router
from .resend_verification import router as resend_verification_router
from .verify_email import router as verify_email_router


router = APIRouter(prefix="/security", tags=["security"])
router.include_router(approve_account_router)
router.include_router(resend_verification_router)
router.include_router(verify_email_router)
