
###################################################################################################
# AIAhura Tech — DevOps Technical Assessment
# Project: AI Inference Service
# This repository is part of AIAhura Tech's DevOps engineer interview process.
# All work submitted will be evaluated for technical quality, security practices, and documentation.
###################################################################################################


# TODO: Implement a Redis-backed rate limiter decorator
# Suggested signature: rate_limiter(max_per_min: int = 60) -> Callable
# Use REDIS_URL env var; fail open if Redis is unavailable.
#raise NotImplementedError("Implement Redis-based rate limiter")
import os
import time
import functools
from typing import Callable
from fastapi import Request, HTTPException
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# اتصال به Redis (fail open: اگر Redis بالا نبود، rate limit اجرا نمی‌شود)
try:
    redis_client = redis.Redis.from_url(REDIS_URL)
    redis_client.ping()
except redis.RedisError:
    redis_client = None

def rate_limiter(max_per_min: int = 60) -> Callable:
    """
    دکوریتور محدودکننده نرخ درخواست بر اساس آدرس IP
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not redis_client:
                # اگر Redis در دسترس نیست، بدون محدودیت اجرا شود
                return await func(*args, **kwargs)

            # گرفتن شیء Request از args یا kwargs
            request: Request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if request is None:
                request = kwargs.get("request")

            if request is None:
                return await func(*args, **kwargs)

            # کلید rate limit برای IP
            client_ip = request.client.host
            key = f"rate_limit:{client_ip}"
            now = int(time.time())

            # چک کردن تعداد درخواست‌ها
            try:
                current_count = redis_client.get(key)
                if current_count is None:
                    # اولین درخواست
                    redis_client.set(key, 1, ex=60)  # expire 60s
                else:
                    current_count = int(current_count)
                    if current_count >= max_per_min:
                        raise HTTPException(status_code=429, detail="Rate limit exceeded")
                    else:
                        redis_client.incr(key)
            except redis.RedisError:
                # Fail open: اگر Redis خطا داد، بدون محدودیت اجرا شود
                return await func(*args, **kwargs)

            return await func(*args, **kwargs)
        return wrapper
    return decorator

