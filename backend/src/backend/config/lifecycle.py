from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.

    This function is used to manage the lifespan of the FastAPI application,
    allowing for setup and teardown operations.

    Args:
        app: The FastAPI application instance.
    """
    logger.info("Starting Nuclera Protein Screening API")
    # Perform any setup operations here (e.g., database connections, etc.)
    try:
        yield
    finally:
        logger.info("Nuclera Protein Screening API has stopped.")
        logger.info("Application is shutting down.")
    # Perform any teardown operations here (e.g., closing database connections, etc.)
