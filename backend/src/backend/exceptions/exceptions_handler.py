
from fastapi import Request, HTTPException 
import logging
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)

def unexpected_exception_handler(request: Request, exc: Exception):
        
        logger.error(
        "Unexpected error | %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
        return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
        },
    )



async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    logger.warning(
        "HTTP error | %s %s | Status: %s | Detail: %s",
        request.method,
        request.url.path,
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
