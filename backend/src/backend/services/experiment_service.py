
import logging
from datetime import datetime, timezone
from uuid import uuid4

from backend.schemas.experiment import Experiment, ExperimentCreate
from backend.services.sequence_validator import SequenceValidator

logger = logging.getLogger(__name__)


class ExperimentService:
    def __init__(self):
        self._experiments: list[Experiment] = []
        self._validator = SequenceValidator()

    def create_experiment(
        self,
        data: ExperimentCreate,
    ) -> Experiment:
        self._validator.validate(data.sequences)
        experiment = Experiment(
            id=uuid4(),
            name=data.name,
            sequences=data.sequences.copy(),
            created_at=datetime.now(timezone.utc),
        )

        self._experiments.append(experiment)

        logger.info("Experiment created: %s", experiment.id)

        return experiment

    def list_experiments(self) -> list[Experiment]:
        return self._experiments.copy()
