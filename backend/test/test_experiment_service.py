from datetime import datetime, timezone
from uuid import UUID

import pytest

from backend.schemas.experiment import ExperimentCreate
from backend.services.experiment_service import ExperimentService
from backend.services.sequence_validator import SequenceValidationError


@pytest.fixture
def service():
    # Fresh in-memory storage for every test
    return ExperimentService()


@pytest.fixture
def valid_sequences():
    # 5-letter prefix, 2-letter variable, 5-letter suffix
    return ["AAAAA" + ("CD" if i % 2 == 0 else "EF") + "GGGGG" for i in range(20)]


@pytest.fixture
def valid_experiment(valid_sequences):
    return ExperimentCreate(
        name="Protein Screening Test",
        sequences=valid_sequences,
    )


# Experiment creation
def test_create_experiment(service, valid_experiment):
    experiment = service.create_experiment(valid_experiment)

    assert isinstance(experiment.id, UUID)
    assert experiment.name == "Protein Screening Test"
    assert experiment.sequences == valid_experiment.sequences
    assert isinstance(experiment.created_at, datetime)
    assert experiment.created_at.tzinfo is not None


def test_created_experiment_is_stored(service, valid_experiment):
    created = service.create_experiment(valid_experiment)

    result = service.list_experiments()

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0].id == created.id


def test_multiple_experiments_have_unique_ids(service, valid_experiment):
    first = service.create_experiment(valid_experiment)
    second = service.create_experiment(valid_experiment)

    assert first.id != second.id


def test_experiment_timestamp_is_utc(service, valid_experiment):
    experiment = service.create_experiment(valid_experiment)

    assert experiment.created_at.utcoffset().total_seconds() == 0


def test_experiment_creation_time(service, valid_experiment):
    before = datetime.now(timezone.utc)

    experiment = service.create_experiment(valid_experiment)

    after = datetime.now(timezone.utc)

    assert before <= experiment.created_at <= after


def test_experiment_sequences_are_copied(service, valid_experiment):
    experiment = service.create_experiment(valid_experiment)

    assert experiment.sequences == valid_experiment.sequences
    assert experiment.sequences is not valid_experiment.sequences


def test_modifying_input_does_not_change_stored_experiment(service, valid_experiment):
    experiment = service.create_experiment(valid_experiment)

    valid_experiment.sequences[0] = "CHANGED"

    assert experiment.sequences[0] != "CHANGED"


# Invalid experiment creation
def test_invalid_experiment_not_stored(service, valid_experiment):
    valid_experiment.sequences.pop()

    with pytest.raises(SequenceValidationError):
        service.create_experiment(valid_experiment)

    result = service.list_experiments()

    assert result["total"] == 0
    assert result["items"] == []


# Listing experiments
def test_list_experiments_empty(service):
    result = service.list_experiments()

    assert result == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def test_list_experiments_returns_all(service, valid_experiment):
    for _ in range(5):
        service.create_experiment(valid_experiment)

    result = service.list_experiments()

    assert result["total"] == 5
    assert len(result["items"]) == 5


# Pagination
@pytest.mark.parametrize(
    "limit,offset,expected_count",
    [
        (5, 0, 5),
        (5, 5, 5),
        (5, 10, 2),
        (20, 0, 12),
        (5, 20, 0),
        (1, 0, 1),
    ],
)
def test_pagination(
    service,
    valid_experiment,
    limit,
    offset,
    expected_count,
):
    for _ in range(12):
        service.create_experiment(valid_experiment)

    result = service.list_experiments(
        limit=limit,
        offset=offset,
    )

    assert len(result["items"]) == expected_count
    assert result["total"] == 12
    assert result["limit"] == limit
    assert result["offset"] == offset


def test_pagination_preserves_creation_order(service, valid_experiment):
    created = [service.create_experiment(valid_experiment) for _ in range(10)]

    result = service.list_experiments(
        limit=3,
        offset=4,
    )

    expected_ids = [experiment.id for experiment in created[4:7]]

    actual_ids = [experiment.id for experiment in result["items"]]

    assert actual_ids == expected_ids


def test_total_count_independent_of_page_size(service, valid_experiment):
    for _ in range(10):
        service.create_experiment(valid_experiment)

    result = service.list_experiments(
        limit=2,
        offset=0,
    )

    assert len(result["items"]) == 2
    assert result["total"] == 10


def test_returned_experiment_isolation(
    service,
    valid_experiment,
):
    service.create_experiment(valid_experiment)

    result = service.list_experiments()

    result["items"][0].name = "Modified Experiment"

    stored = service.list_experiments()

    assert stored["items"][0].name == "Protein Screening Test"
