# -*- coding=utf-8 -*-
r"""

"""
from app.config import SETTINGS
from .lib import ClamAVAsyncClient, ScanResult, AsyncReadableBuffer


__all__ = ['SUPPORTED', 'scan_abuffer']


SUPPORTED: bool = SETTINGS.CLAMAV is not None


def _get_client() -> ClamAVAsyncClient:
    return ClamAVAsyncClient(host=SETTINGS.CLAMAV.SERVER, port=SETTINGS.CLAMAV.PORT)


async def scan_abuffer(buffer: AsyncReadableBuffer) -> ScanResult:
    if not SUPPORTED:
        raise RuntimeError("No MAIL configured")

    client = _get_client()
    return await client.scan_abuffer(buffer=buffer)
