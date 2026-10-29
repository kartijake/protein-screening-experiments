from fastapi import FastAPI
from backend.middleware import initialise_middleware
from backend.api.v1 import router as api_v1_router
from backend.config.lifecycle import lifespan
from backend.exceptions import initialise_exception_handlers

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app = FastAPI(title="Nuclera Protein Screening API", version="1.0.0",lifespan=lifespan)

initialise_middleware(app)
initialise_exception_handlers(app)
app.include_router(api_v1_router)

