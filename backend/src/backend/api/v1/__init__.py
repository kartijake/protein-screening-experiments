from fastapi import APIRouter
from .experiment_route import router as experiment_router

router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)
router.include_router(experiment_router)
