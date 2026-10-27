
from fastapi import APIRouter, status

from backend.schemas.experiment import Experiment, ExperimentCreate
from backend.services import experiment_service

router = APIRouter(
    prefix="/experiments",
    tags=["Experiments"],
)


@router.post(
    "",
    response_model=Experiment,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(data: ExperimentCreate):
    return experiment_service.create_experiment(data)


@router.get(
    "",
    response_model=list[Experiment],
)
def list_experiments():
    return experiment_service.list_experiments()
