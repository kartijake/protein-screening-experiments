from fastapi import APIRouter
from .health_route import router as health_router

router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

router.include_router(health_router)