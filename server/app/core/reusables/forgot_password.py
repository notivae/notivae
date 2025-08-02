# -*- coding=utf-8 -*-
r"""

"""
from urllib.parse import urlencode
from fastapi import Request
from uuid import UUID
from app.services.mail import LocalForgotPasswordParameters, send_local_forgot_password_email as _send_local_forgot_password_email
from app.core.security.local import generate_local_password_reset_token


__all__ = ['send_local_forgot_password_email']


async def send_local_forgot_password_email(request: Request, user_id: UUID, user_email: str):
    token = generate_local_password_reset_token(user_id=user_id)

    ui_path = "/auth/local/forgot-password"
    query = dict(
        token=token,
    )

    reset_url = f"{request.base_url}#{ui_path}?{urlencode(query=query)}"

    parameters = LocalForgotPasswordParameters(
        reset_url=reset_url,
    )

    await _send_local_forgot_password_email(
        to=user_email,
        parameters=parameters,
        request=request,
    )
