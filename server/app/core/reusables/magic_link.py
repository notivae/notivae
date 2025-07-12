# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request
from app.db.models import User
from app.services.mail import MagicLinkParameters, send_magic_link_email as _send_magic_link_email
from app.core.security.magic_link import generate_magic_link_token


__all__ = ['send_magic_link_email']


async def send_magic_link_email(request: Request, user: User):
    token = generate_magic_link_token(user_id=user.id)

    parameters = MagicLinkParameters(
        callback_url=str(request.url_for('magic_callback').include_query_params(token=token)),
        username=user.name,
        display_name=user.display_name,
    )

    await _send_magic_link_email(
        to=user.email,
        parameters=parameters,
        request=request,
    )
