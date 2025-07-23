# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import structlog
from fastapi import Request
import sqlalchemy as sql
from app.services.mail import AdminAccountApprovalParameters, send_admin_account_approval_email as _send_admin_account_approval_email
from app.core.security.account_approval import generate_account_approval_token
from app.db.session import AsyncSessionLocal
from app.db.models import User


__all__ = ['send_admin_account_approval_email']

logger: structlog.BoundLogger = structlog.get_logger()


async def send_admin_account_approval_email(request: Request, user: User):
    async with AsyncSessionLocal() as session:
        stmt = sql.select(User).where(User.is_system_admin.is_(True))
        admin_accounts: t.Iterable[User] = await session.scalars(stmt)
        to = [admin.email for admin in admin_accounts]
        if not to:
            logger.warning("no-admin-accounts", message="no admin-accounts found. can't send account approval email")
            return

    token = generate_account_approval_token(user_id=user.id)

    parameters = AdminAccountApprovalParameters(
        approval_url=str(request.url_for('account_approval_via_token').include_query_params(token=token)),
        account_email=user.email,
        account_name=user.name,
        account_display_name=user.display_name,
    )

    await _send_admin_account_approval_email(
        to=to,
        parameters=parameters,
        request=request,
    )
