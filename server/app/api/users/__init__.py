# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .avatars import router as avatars_router


router = APIRouter(prefix="/users", tags=["users"])
router.include_router(avatars_router)
