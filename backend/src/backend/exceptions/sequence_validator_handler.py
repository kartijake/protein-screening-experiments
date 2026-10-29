from fastapi import Request, status
from backend.services.sequence_validator import SequenceValidationError
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


def sequence_validator(request: Request, exc: SequenceValidationError):
    logger.warning(
        "Amino acid sequence error | %s %s | RID:%s | Error: %s",
        request.method,
        request.url.path,
        getattr(request.state, "request_id", "unknown"),
        exc,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": str(exc)},
    )
