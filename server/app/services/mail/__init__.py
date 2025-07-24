# -*- coding=utf-8 -*-
r"""

"""
from .core import SUPPORTED
from .abstracts import (
    TestParameters, send_test_email,
    MailVerificationParameters, send_verification_email,
    MagicLinkParameters, send_magic_link_email,
    MFAEnabledParameters, send_mfa_enabled_email,
    NewNotificationParameters, send_new_notification_email,
    AdminAccountApprovalParameters, send_admin_account_approval_email,
)


__all__ = [
    'SUPPORTED',
    'TestParameters', 'send_test_email',
    'MailVerificationParameters', 'send_verification_email',
    'MagicLinkParameters', 'send_magic_link_email',
    'MFAEnabledParameters', 'send_mfa_enabled_email',
    'NewNotificationParameters', 'send_new_notification_email',
    'AdminAccountApprovalParameters', 'send_admin_account_approval_email',
]
