# -*- coding=utf-8 -*-
r"""

"""
import httpx
from ..redis import redis_client
from ..structures import OpenIdConfiguration


CONFIG_TTL = 3600  # 1h


async def get_configuration(discovery_uri: str) -> OpenIdConfiguration:
    cache_key = f"openid:config:{discovery_uri}"

    cached = await redis_client.get(cache_key)
    if cached:
        return OpenIdConfiguration.model_validate_json(cached)

    async with httpx.AsyncClient() as client:
        response = await client.get(url=str(discovery_uri), timeout=10)
        response.raise_for_status()
        config = OpenIdConfiguration.model_validate_json(response.content)

    await redis_client.set(cache_key, config.model_dump_json(), ex=CONFIG_TTL)

    return config
