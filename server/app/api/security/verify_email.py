# -*- coding=utf-8 -*-
r"""

"""
import structlog
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import ValidationError
from jose import JWTError, ExpiredSignatureError
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session
from app.db.models import User
from app.core.security.email_verification import parse_email_verification_token


router = APIRouter()
logger = structlog.get_logger()


@router.get('/verify-email')
async def verify_email(
        session: AsyncSession = Depends(get_async_session),
        token: str = Query(),
) -> dict:
    r"""
    Validates a user based on a JWT.

    The request will fail if the token is expired, invalid or the user does no longer exist.
    """
    try:
        claims = parse_email_verification_token(token=token)
    except ExpiredSignatureError:
        logger.warning("expired-token", message="Expired token received")
        raise HTTPException(  # todo: proper redirect to page with "resend verification mail" button
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The token has expired",
        )
    except (JWTError, ValidationError) as e:
        logger.error("invalid-token", message=f"{type(e)}: {e}", token=token)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token received",
        )

    stmt = sql.select(User).where(User.id == claims.sub)
    user: User = await session.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.email_verified = True
    await session.commit()

    return { 'success': True }  # todo: better success handling
