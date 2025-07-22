# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import secrets
import string


__all__ = ['generate_backup_codes']


def generate_backup_codes(count: int, length: int = 8) -> t.List[str]:
    codes: t.Set[str] = set()
    alphabet = string.ascii_uppercase + string.digits

    while len(codes) < count:
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        codes.add(code)

    return list(codes)
