# -*- coding=utf-8 -*-
r"""

"""
import structlog
from fastapi import APIRouter, HTTPException, status, Request, Depends, Body
from jose import JWTError
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ValidationError
from app.core.dependencies import get_async_session, get_current_user_optional
from app.core.security.email_verification import parse_email_verification_token
from app.services.mail import SUPPORTED as MAIL_SUPPORTED
from app.core.reusables.verification_mail import send_verification_email
from app.db.models import User


router = APIRouter()
logger = structlog.get_logger()


class ResendVerificationResponse(BaseModel):
    message: str


@router.post("/resend-verification", response_model=ResendVerificationResponse)
async def resend_email_verification(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        token: str = Body(default=None, embed=True),
        user: User = Depends(get_current_user_optional),
):
    r"""
    re-sends a verification email based on
    A) a JWT that would normally be used for `/api/security/verify-email`
    B) the currently logged-in user

    The request will fail if:
    - the mail-service is currently not supported
    - no user is logged in, or no token is provided
    - the token is invalid
    - user does not exist
    - user-email is already verified
    """
    if not MAIL_SUPPORTED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The email verification service is not available",
        )

    if token is None and user is None:
        logger.warning("No token received and no user is logged in")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication",
        )
    elif token is not None:
        try:
            claims = parse_email_verification_token(token=token, ignore_expired=True)
        except (JWTError, ValidationError) as e:
            logger.error(f"invalid-token ({type(e)}: {e})", exc_info=e, token=token)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token received",
            )

        if user and str(user.id) != claims.sub:
            logger.warning("Logged in user tried to resend verification email for different subject", user=user.id, subject=claims.sub)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User does not have access to this token",
            )

        stmt = sql.select(User).where(User.id == claims.sub)
        user: User = await session.scalar(stmt)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already verified",
        )

    try:
        await send_verification_email(request=request, user=user)
    except Exception as e:
        logger.error(f"failed to re-send verification ({type(e)}: {e})", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email",
        )

    logger.info("re-send verification email for user", user=user.id)

    return ResendVerificationResponse(message="Email verification sent")
