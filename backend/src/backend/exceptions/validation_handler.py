
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import logging
logger = logging.getLogger(__name__)

async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []
    for error in exc.errors():
        field = ".".join(str(part) for part in error["loc"])
        message = error["msg"]
        if field == "body" and error["type"] == "missing":
             message = "Request body is required"
        errors.append({"field": field, "message": message})

    logger.warning(
        "Request validation failed | %s %s | RID:%s | Errors: %s",
        request.method,
        request.url.path,
        getattr(request.state, "request_id", "unknown"),
        len(errors),
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": errors,
        },
    )
