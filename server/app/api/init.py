# -*- coding=utf-8 -*-
r"""

"""
from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import BaseModel, EmailStr
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_async_session, rate_limited
from app.db.models import User, AuthIdentity
from app.core.security.local import hash_password
from app.api.auth.local._common import AuthLocalIdentityContext


router = APIRouter(tags=["Setup"])


global_is_initialized: bool = False


@router.get(
    path="/init-completed",
    response_model=bool,
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/300))],
)
async def server_init_completed(
    session: AsyncSession = Depends(get_async_session),
):
    global global_is_initialized
    if global_is_initialized:
        return True

    stmt = sql.select(User).where(User.is_system_admin.is_(True)).limit(1)
    global_is_initialized = (await session.scalar(stmt)) is not None
    return global_is_initialized


class AdminAccountDetails(BaseModel):
    username: str
    display_name: str | None
    email: EmailStr
    password: str


class InitRequest(BaseModel):
    admin_account: AdminAccountDetails


@router.post(
    path="/init",
    dependencies=[Depends(rate_limited(capacity=5, refill_rate=1/300))],
)
async def server_init(
        session: AsyncSession = Depends(get_async_session),
        form: InitRequest = Body()
):
    stmt = sql.select(User.id).where(User.is_system_admin.is_(True)).limit(1)
    system_administrator_exists = (await session.scalar(stmt)) is not None
    if system_administrator_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System already initialized",
        )

    admin_user = User(
        email=str(form.admin_account.email),
        name=form.admin_account.name,
        display_name=form.admin_account.display_name,
        is_approved=True,
        is_system_admin=True,
    )
    session.add(admin_user)
    await session.flush()

    context = AuthLocalIdentityContext(
        password_hashed=hash_password(form.admin_account.password),
    )

    auth_identity = AuthIdentity(
        user_id=admin_user.id,
        provider="local",
        provider_user_id=admin_user.name,
        provider_email=admin_user.email,
        context=context.model_dump(mode="json"),
    )
    session.add(auth_identity)

    await session.commit()
