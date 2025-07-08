# -*- coding=utf-8 -*-
r"""

"""
import structlog
from fastapi import HTTPException, status, Depends
from app.db.models import User
from .user import get_current_user


__all__ = ['require_system_admin']


logger: structlog.BoundLogger = structlog.get_logger()


async def require_system_admin(
        user: User = Depends(get_current_user),
):
    if not user.is_system_admin:
        logger.warning(message="Unauthorized access", user=user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a system administrator",
        )
