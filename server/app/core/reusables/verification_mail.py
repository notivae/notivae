# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request
from app.db.models import User
from app.services.mail import MailVerificationParameters, send_verification_email as _send_verification_email
from app.core.security.email_verification import generate_email_verification_token


__all__ = ['send_verification_email']


async def send_verification_email(request: Request, user: User):
    token = generate_email_verification_token(user_id=user.id)

    parameters = MailVerificationParameters(
        verification_url=str(request.url_for('verify_email').include_query_params(token=token)),
        username=user.name,
        display_name=user.display_name,
    )

    await _send_verification_email(
        to=user.email,
        parameters=parameters,
        request=request,
    )
