# -*- coding=utf-8 -*-
r"""

"""
from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .async_session import get_async_session
from ..security.rate_limiting import check_is_rate_limited, get_rate_limit_key


__all__ = ['rate_limited']


def rate_limited(*, capacity: int, refill_rate: float, group: str = None):
    r"""

    :param capacity: maximum number of requests allowed at once
    :param refill_rate: time in seconds between adding a token to the bucket
    :param group: identifier. Fallback to endpoint function name
    """

    async def limiter_dependency(request: Request, response: Response, session: AsyncSession = Depends(get_async_session)):
        group_key = group
        if group_key is None:
            endpoint_function = request.scope.get('endpoint')
            group_key = getattr(endpoint_function, '__name__', None)

        key = await get_rate_limit_key(request=request, session=session, group=group_key)
        is_limited, headers = await check_is_rate_limited(key=key, capacity=capacity, refill_rate=refill_rate)
        if is_limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers=headers,
            )
        response.headers.update(headers)

    return limiter_dependency
