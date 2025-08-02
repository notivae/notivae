# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .account import router as account_router
from .auth_identities import router as auth_identities_router


router = APIRouter(prefix="/me", tags=["User Me"])
router.include_router(auth_identities_router)
router.include_router(account_router)
