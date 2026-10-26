
from fastapi import FastAPI
from starlette.exceptions import HTTPException

from .exceptions_handler import (
    http_exception_handler,
    unexpected_exception_handler,
)


def initialise_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )
