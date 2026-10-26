
import logging
import time
from uuid import uuid4

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    request_id = str(uuid4())
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "[%s] %s %s | Status: %s | Duration: %.2fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception:
        logger.exception(
            "[%s] %s %s | Request failed",
            request_id,
            request.method,
            request.url.path,
        )
        raise
