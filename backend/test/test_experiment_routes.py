import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.main import app
from backend.services import experiment_service


@pytest.fixture
def client(monkeypatch):
    # Isolate in-memory experiments for each test.
    # Preserve the original list after the test.
    monkeypatch.setattr(
        experiment_service,
        "_experiments",
        [],
    )

    with TestClient(app, base_url="http://testserver/api/v1") as test_client:
        yield test_client


@pytest.fixture
def valid_sequences():
    return ["AAAAA" + ("CD" if i % 2 == 0 else "EF") + "GGGGG" for i in range(20)]


@pytest.fixture
def valid_payload(valid_sequences):
    return {
        "name": "Protein Screening Test",
        "sequences": valid_sequences,
    }


@pytest.fixture
def valid_fasta(valid_sequences):
    return "\n".join(
        f">SEQUENCE_{i}\n{sequence}"
        for i, sequence in enumerate(valid_sequences, start=1)
    ).encode("utf-8")


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


# POST /experiments


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
        " \t\n ",
    ],
)
def test_create_experiment_blank_name(
    client,
    valid_payload,
    invalid_name,
):
    valid_payload["name"] = invalid_name

    response = client.post(
        "/experiments",
        json=valid_payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    data = response.json()

    assert data["error"] == "Validation failed"
    assert any(
        detail["field"] == "body.name"
        and "Experiment name is required" in detail["message"]
        for detail in data["details"]
    )


def test_create_experiment(client, valid_payload):
    response = client.post(
        "/experiments",
        json=valid_payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["name"] == valid_payload["name"]
    assert data["sequences"] == valid_payload["sequences"]
    assert "id" in data
    assert "created_at" in data


def test_create_experiment_invalid_count(client, valid_payload):
    valid_payload["sequences"].pop()

    response = client.post(
        "/experiments",
        json=valid_payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_experiment_missing_name(client, valid_sequences):
    response = client.post(
        "/experiments",
        json={"sequences": valid_sequences},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_experiment_missing_sequences(client):
    response = client.post(
        "/experiments",
        json={"name": "Test"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.parametrize(
    "payload",
    [
        {},
        [],
        None,
        "invalid",
        123,
        True,
    ],
)
def test_create_experiment_invalid_body(client, payload):
    response = client.post(
        "/experiments",
        json=payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# ----------------------------------
# GET /experiments
# ----------------------------------


def test_list_experiments_empty(client):
    response = client.get("/experiments")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def test_create_then_list(client, valid_payload):
    create_response = client.post(
        "/experiments",
        json=valid_payload,
    )

    assert create_response.status_code == status.HTTP_201_CREATED

    created_id = create_response.json()["id"]

    list_response = client.get("/experiments")

    assert list_response.status_code == status.HTTP_200_OK

    data = list_response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == created_id


@pytest.mark.parametrize(
    "limit,offset,expected_count",
    [
        (5, 0, 5),
        (5, 5, 5),
        (5, 10, 2),
        (20, 0, 12),
        (5, 20, 0),
    ],
)
def test_list_pagination(client, valid_payload, limit, offset, expected_count):
    for _ in range(12):
        response = client.post(
            "/experiments",
            json=valid_payload,
        )
        assert response.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/experiments",
        params={"limit": limit, "offset": offset},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["total"] == 12
    assert len(data["items"]) == expected_count
    assert data["limit"] == limit
    assert data["offset"] == offset


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0, "offset": 0},
        {"limit": -1, "offset": 0},
        {"limit": 101, "offset": 0},
        {"limit": 10, "offset": -1},
        {"limit": "abc", "offset": 0},
        {"limit": 10, "offset": "abc"},
    ],
)
def test_invalid_pagination(client, params):
    response = client.get(
        "/experiments",
        params=params,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# ----------------------------------
# POST /experiments/uplaod
# ----------------------------------

UPLOAD_URL = "/experiments/upload"


def upload_file(client, content, name="FASTA Test"):
    return client.post(
        UPLOAD_URL,
        data={"name": name},
        files={
            "file": (
                "proteins.fasta",
                content,
                "text/plain",
            )
        },
    )


def test_upload_valid_fasta(client, valid_fasta):
    response = upload_file(client, valid_fasta)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["name"] == "FASTA Test"
    assert len(data["sequences"]) == 20
    assert "id" in data


def test_upload_then_fetch(client, valid_fasta):
    upload_response = upload_file(client, valid_fasta)

    assert upload_response.status_code == status.HTTP_200_OK

    created_id = upload_response.json()["id"]

    response = client.get("/experiments")

    assert response.status_code == status.HTTP_200_OK

    items = response.json()["items"]

    assert len(items) == 1
    assert items[0]["id"] == created_id


def test_upload_missing_file(client):
    response = client.post(
        UPLOAD_URL,
        data={"name": "Test"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_upload_missing_name(client, valid_fasta):
    response = client.post(
        UPLOAD_URL,
        files={
            "file": (
                "test.fasta",
                valid_fasta,
                "text/plain",
            )
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_upload_oversized_file(client):
    content = b"A" * (32 * 1024 + 1)

    response = upload_file(client, content)

    assert response.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    assert response.json()["error"] == "File too large"


def test_upload_invalid_encoding(client):
    content = b"\xff\xfe\xfa\xfb"

    response = upload_file(client, content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"] == "Invalid text encoding"


def test_upload_invalid_fasta(client):
    content = b">SEQUENCE_1\nINVALID123"

    response = upload_file(client, content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_upload_empty_file(client):
    response = upload_file(client, b"")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_upload_invalid_sequence_count(client):
    content = "\n".join(f">SEQ_{i}\nAAAAACDGGGGG" for i in range(19)).encode("utf-8")

    response = upload_file(client, content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"] == ("Exactly 20 sequences required")
