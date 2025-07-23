# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter
from .delete import router as delete_router
from .get import router as get_router
from .patch import router as patch_router


router = APIRouter(prefix='/notifications', tags=['Notifications'])
router.include_router(delete_router)
router.include_router(get_router)
router.include_router(patch_router)
