"""
AfriLang – Rate limiting middleware.

Uses a simple in-memory sliding-window counter keyed on the API key name.
Drop-in Redis replacement: swap _get_counter / _set_counter with redis.incr/expire.

Limits (configurable via env):
  RATE_LIMIT_RPM        – requests per minute for /translate
  RATE_LIMIT_BATCH_RPM  – requests per minute for /translate/batch
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Dict, Deque

from fastapi import HTTPException, Request, status

from app.core.config import settings


# ── In-memory sliding-window store ───────────────────────────────────────────
# { "key_name:endpoint_group" -> deque of request timestamps }
_WINDOWS: Dict[str, Deque[float]] = defaultdict(deque)


def _sliding_window_check(bucket: str, limit: int, window_seconds: int = 60) -> int:
    """
    Returns remaining requests in window.
    Raises HTTP 429 if limit exceeded.
    """
    now = time.monotonic()
    q = _WINDOWS[bucket]

    # Remove timestamps outside the current window
    while q and q[0] < now - window_seconds:
        q.popleft()

    if len(q) >= limit:
        retry_after = int(window_seconds - (now - q[0])) + 1
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": str(retry_after)},
            detail={
                "code": "RATE_LIMIT_EXCEEDED",
                "message": (
                    f"Rate limit of {limit} requests/minute exceeded. "
                    f"Retry after {retry_after} seconds."
                ),
                "retry_after_seconds": retry_after,
            },
        )

    q.append(now)
    return limit - len(q)


def check_rate_limit(key_record: dict, endpoint_group: str = "default") -> None:
    """
    Call from any protected endpoint handler after injecting `require_api_key`.

    endpoint_group: "translate" | "batch" | "speech"
    """
    name = key_record.get("name", "unknown")
    bucket = f"{name}:{endpoint_group}"

    limit_map = {
        "translate": settings.rate_limit_rpm,
        "batch":     settings.rate_limit_batch_rpm,
        "speech":    settings.rate_limit_rpm,
        "default":   settings.rate_limit_rpm,
    }
    limit = limit_map.get(endpoint_group, settings.rate_limit_rpm)
    _sliding_window_check(bucket, limit)
