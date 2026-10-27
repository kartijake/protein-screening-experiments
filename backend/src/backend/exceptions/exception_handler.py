
from fastapi import Request 
import logging
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)

def unexpected_exception_handler(request: Request, exc: Exception):
        
        logger.error(
        "Unexpected error | %s %s | RID:%s",
        request.method,
        request.url.path,
        getattr(request.state, "request_id", "unknown"),
        exc_info=(type(exc), exc, exc.__traceback__),
    )
        return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
        },
    )



