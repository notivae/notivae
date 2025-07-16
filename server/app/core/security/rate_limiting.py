# -*- coding=utf-8 -*-
r"""

"""
import time
import math
import datetime as dt
import typing as t
from fastapi import Request
import redis.exceptions
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.db.models import AuthSession
from ..util import get_client_ip
from .auth_session import hash_session_token


__all__ = ['check_is_rate_limited', 'get_rate_limit_key']


LUA_SHA = ""

LUA_BUCKET_SCRIPT = """
local token_key = KEYS[1]
local ts_key = KEYS[2]

local now = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local refill_rate = tonumber(ARGV[3])
local ttl = tonumber(ARGV[4])

local tokens = tonumber(redis.call("get", token_key)) or capacity
local last_ts = tonumber(redis.call("get", ts_key)) or now

local elapsed = now - last_ts
local new_tokens = math.min(capacity, tokens + elapsed * refill_rate)

local is_limited = 1
if new_tokens >= 1 then
    new_tokens = new_tokens - 1
    is_limited = 0
end

redis.call("setex", token_key, ttl, new_tokens)
redis.call("setex", ts_key, ttl, now)

-- converting `new_tokens`::FLOAT to its string representation. Otherwise redis would cast to ::INTEGER
-- but we need ::FLOAT to properly calculate the `Retry-After` header
return {is_limited, string.format("%.6f", new_tokens)}
"""


async def load_script():
    global LUA_SHA
    LUA_SHA = await redis_client.script_load(script=LUA_BUCKET_SCRIPT)


async def check_is_rate_limited(key: str, capacity: int, refill_rate: float) -> t.Tuple[bool, dict]:
    r"""
    Uses a Redis Lua script to safely apply token bucket rate limiting.
    """
    now = time.time()
    ttl = math.ceil(capacity / refill_rate)

    tokens_key = f"{key}:tkn"
    ts_key = f"{key}:ts"

    keys = [tokens_key, ts_key]
    args = [now, capacity, refill_rate, ttl]
    try:
        is_limited, tokens_str = await redis_client.evalsha(LUA_SHA, len(keys), *keys, *args)
    except redis.exceptions.NoScriptError:
        await load_script()
        is_limited, tokens_str = await redis_client.evalsha(LUA_SHA, len(keys), *keys, *args)
    tokens = float(tokens_str)

    headers = {
        'X-RateLimit-Limit': str(capacity),
        'X-RateLimit-Remaining': str(int(tokens)),
    }

    if is_limited:
        # todo: cound violations in a time-window and report or issue temp-ban
        retry = math.ceil((1 - tokens) / refill_rate)
        headers['Retry-After'] = str(int(retry))

    return is_limited, headers


async def ensure_valid_auth_token(session: AsyncSession, hashed_token: str) -> bool:
    r"""
    Ensures a given auth-session token-hash exists with a valid entry in the database.
    This is only a quick check via redis-cache.

    Note: after revoking an auth-session it can take up to `max_ttl` before the auth-session stops working
    """
    max_ttl = 60

    key = f"ht:{hashed_token}"
    cached = await redis_client.get(key)
    if cached is not None:
        return bool(cached)

    stmt = sql.select(AuthSession).where(AuthSession.hashed_token == hashed_token)
    auth_session: AuthSession = await session.scalar(stmt)

    now = dt.datetime.now(dt.UTC)
    valid_token = not (
            auth_session is None
            or auth_session.revoked
            or auth_session.expires_at < now
    )
    ttl = min((auth_session.expires_at - now).total_seconds(), max_ttl) if auth_session else max_ttl

    await redis_client.set(key, int(valid_token), ex=ttl)
    return valid_token


async def get_rate_limit_key(request: Request, session: AsyncSession, group: str) -> str:
    r"""
    Finds the rate-limit key for a given request. If someone is logged in with a valid session, then that's the identifier.
    Otherwise, we will use their IP address
    """
    session_token = request.cookies.get('session_token')
    if session_token:
        hashed = hash_session_token(session_token)
        if await ensure_valid_auth_token(session=session, hashed_token=hashed):
            return f"rl:tkn:{hashed}:{group}"
    return f"rl:ip:{get_client_ip(request=request)}:{group}"
