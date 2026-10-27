from fastapi import Request,HTTPException 
import logging
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    logger.warning(
        "HTTP error | %s %s | RID:%s | Status: %s | Detail: %s",
        request.method,
        request.url.path,
        getattr(request.state, "request_id", "unknown"),
        exc.status_code,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
        },
        headers=exc.headers,
    )
