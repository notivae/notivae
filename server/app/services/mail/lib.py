# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from email.utils import formataddr
from pydantic import EmailStr, NameEmail, validate_email


__all__ = ['AnyMailAddress', 'TO', 'normalize_to', 'extract_mail_address']


AnyMailAddress: t.TypeAlias = t.Union[EmailStr, t.Tuple[t.Optional[str], EmailStr], t.Tuple[t.Optional[str], str], NameEmail, str]
TO: t.TypeAlias = t.Union[AnyMailAddress, t.List[AnyMailAddress]]


def normalize_to(to: TO) -> t.Union[str, t.List[str]]:
    if isinstance(to, list):
        return [normalize_to(_) for _ in to]
    if isinstance(to, tuple):
        return formataddr((to[0], str(to[1])))
    return str(to)


def extract_mail_address(to: TO) -> t.Union[str, t.List[str]]:
    normalized = normalize_to(to)
    if isinstance(normalized, list):
        return [validate_email(n)[1] for n in normalized]
    return validate_email(normalized)[1]
