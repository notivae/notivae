# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from urllib.parse import urljoin
from pydantic import BaseModel, HttpUrl
from fastapi import Request
from .core import render_template, send_email
from .lib import TO, extract_mail_address


__all__ = [
    'TestParameters', 'send_test_email',
    'MailVerificationParameters', 'send_verification_email',
]


async def _send_mail(template: str, to: TO, subject: str, parameters: BaseModel, request: Request = None):
    context = parameters.model_dump()
    if request is not None:
        context.update(logo_url=urljoin(str(request.base_url), 'logo.svg'))
    if isinstance(recipient_email := extract_mail_address(to), str):  # currently only for single mails
        context.update(recipient_email=recipient_email)
    html_body = await render_template(name=template, context=context)
    await send_email(to=to, subject=subject, html_body=html_body)


class TestParameters(BaseModel):
    pass


async def send_test_email(
        to: TO,
        parameters: TestParameters,
        request: Request = None,
):
    await _send_mail(
        template="test.html.j2",
        to=to,
        subject="Test email",
        parameters=parameters,
        request=request,
    )


class MailVerificationParameters(BaseModel):
    verification_url: HttpUrl
    username: str
    display_name: t.Optional[str]


async def send_verification_email(
        to: TO,
        parameters: MailVerificationParameters,
        request: Request = None,
):
    await _send_mail(
        template="mail-verification.html.j2",
        to=to,
        subject="Mail Verification",
        parameters=parameters,
        request=request,
    )
