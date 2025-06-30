# -*- coding=utf-8 -*-
r"""

"""
import httpx
from ..redis import redis_client
from ..structures import OpenIDConfiguration, OpenIDJwkKeys


CONFIG_TTL = 3600  # 1h
JWK_TTL = 900  # 15 min


async def get_configuration(discovery_uri: str) -> OpenIDConfiguration:
    cache_key = f"openid:config:{discovery_uri}"

    cached = await redis_client.get(cache_key)
    if cached:
        return OpenIDConfiguration.model_validate_json(cached)

    async with httpx.AsyncClient() as client:
        response = await client.get(url=str(discovery_uri), timeout=10)
        response.raise_for_status()
        config = OpenIDConfiguration.model_validate_json(response.content)

    await redis_client.set(cache_key, config.model_dump_json(), ex=CONFIG_TTL)

    return config


async def get_jwk(discovery_uri: str) -> OpenIDJwkKeys:
    cache_key = f"openid:jwk:{discovery_uri}"

    cached = await redis_client.get(cache_key)
    if cached:
        return OpenIDJwkKeys.model_validate_json(cached)

    jwk_uri = (await get_configuration(discovery_uri=discovery_uri)).jwks_uri

    async with httpx.AsyncClient() as client:
        response = await client.get(url=str(jwk_uri), timeout=10)
        response.raise_for_status()
        jwk = OpenIDJwkKeys.model_validate_json(response.content)

    await redis_client.set(cache_key, jwk.model_dump_json(), ex=JWK_TTL)

    return jwk
