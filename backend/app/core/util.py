# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request


__all__ = ['get_client_ip']


def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip

    envoy_ip = request.headers.get("X-Envoy-External-Address")
    if envoy_ip:
        return envoy_ip

    return request.client.host
