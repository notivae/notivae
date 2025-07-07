# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .auth_identities import router as auth_identities_router
from .me import router as me_router


router = APIRouter(prefix="/user", tags=["User"])
router.include_router(auth_identities_router)
router.include_router(me_router)
