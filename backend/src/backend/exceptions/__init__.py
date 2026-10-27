
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from .exception_handler import unexpected_exception_handler
from .http_handler import http_exception_handler
from .validation_handler import request_validation_exception_handler
from .sequence_validator_handler import sequence_validator
from backend.services.sequence_validator import SequenceValidationError


def initialise_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler
        )

    app.add_exception_handler(SequenceValidationError,sequence_validator)

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )
    