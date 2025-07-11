# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from urllib.parse import urljoin
from pydantic import BaseModel, HttpUrl, EmailStr
from fastapi import Request
from .core import render_template, send_email, SUPPORTED
from .lib import TO, extract_mail_addresses


__all__ = [
    'TestParameters', 'send_test_email',
    'MailVerificationParameters', 'send_verification_email',
    'AdminAccountApprovalParameters', 'send_admin_account_approval_email',
]


async def _send_mail(template: str, to: TO, subject: str, parameters: BaseModel, request: Request = None):
    if not SUPPORTED: return

    context = parameters.model_dump()
    if request is not None:
        context.update(logo_url=urljoin(str(request.base_url), 'logo.svg'))
    recipients = extract_mail_addresses(to)
    if len(recipients) == 1:
        context.update(recipient_email=recipients[0])
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


class AdminAccountApprovalParameters(BaseModel):
    approval_url: HttpUrl
    account_email: EmailStr
    account_name: str
    account_display_name: t.Optional[str]


async def send_admin_account_approval_email(
        to: TO,
        parameters: AdminAccountApprovalParameters,
        request: Request = None,
):
    await _send_mail(
        template="admin-account-approval.html.j2",
        to=to,
        subject="Admin Account Approval",
        parameters=parameters,
        request=request,
    )
