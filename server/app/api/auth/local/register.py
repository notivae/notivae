# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Request, Depends, Body, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, get_current_user_optional
from app.core.security.passwords import hash_password
from app.db.models import User, AuthIdentity
from app.config import SETTINGS, AccountCreationMode
from app.core.reusables.verification_mail import send_verification_email
from app.core.reusables.account_approval import send_admin_account_approval_email
from ._common import AuthLocalIdentityContext


router = APIRouter()


class RegisterRequest(BaseModel):
    username: str = Field(..., pattern=r"^[a-z0-9_-]+$", max_length=32)
    display_name: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def auth_local_register(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user_optional),
        form_data: RegisterRequest = Body(),
):
    if SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account creation is currently closed",
        )

    if user:
        stmt = sql.select(AuthIdentity).where(AuthIdentity.provider == "local", AuthIdentity.user_id == user.id)
        identity: AuthIdentity = await session.scalar(stmt)
        if identity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered",
            )

    stmt = sql.select(AuthIdentity) \
        .where(AuthIdentity.provider == "local",
               sql.or_(
                   AuthIdentity.provider_user_id == form_data.username,
                   AuthIdentity.provider_email == form_data.email
               ))
    identity: AuthIdentity = await session.scalar(stmt)
    if identity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )

    if user is None:
        user = User(
            email=str(form_data.email),
            name=form_data.username,
            display_name=form_data.display_name,
            is_approved=SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.OPEN,
        )
        session.add(user)
        await session.flush()

        background_tasks.add_task(send_verification_email, request=request, user=user)
        if SETTINGS.APP.ACCOUNT_CREATION == AccountCreationMode.RESTRICTED:
            background_tasks.add_task(send_admin_account_approval_email, request=request, user=user)

    context = AuthLocalIdentityContext(
        password_hashed=hash_password(plain_password=form_data.password),
    )

    identity = AuthIdentity(
        user_id=user.id,
        provider="local",
        provider_user_id=form_data.username,
        provider_email=str(form_data.email),
        context=context.model_dump(mode='json'),
    )
    session.add(identity)
    await session.commit()
