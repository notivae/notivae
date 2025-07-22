# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request
from app.db.models import User
from app.services.mail import MFAEnabledParameters, send_mfa_enabled_email as _send_mfa_enabled_email


__all__ = ['send_mfa_enabled_email']


async def send_mfa_enabled_email(request: Request, user: User):
    parameters = MFAEnabledParameters(
        username=user.name,
        display_name=user.display_name,
    )

    await _send_mfa_enabled_email(
        to=user.email,
        parameters=parameters,
        request=request,
    )
