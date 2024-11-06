import pytest
from fastapi.testclient import TestClient

from backend.passphrases import Passphrases


def test_valid_sqli1_submission(client: TestClient) -> None:
    response = client.post(
        "/submission", json={"challenge": "sqli1", "secret": Passphrases.sqli1.value}
    )
    assert response.status_code == 200
    assert response.json() == {"result": True}


def test_invalid_sqli1_submission(client: TestClient) -> None:
    response = client.post(
        "/submission", json={"challenge": "sqli1", "secret": "wrong_secret"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": False}


def test_invalid_challenge(client: TestClient) -> None:
    response = client.post(
        "/submission", json={"challenge": "nonexistent", "secret": "any_secret"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": False, "message": "Invalid challenge"}


@pytest.mark.parametrize("challenge_name", ["sqli1", "sqli2", "ssrf1", "ssrf2"])
def test_all_challenges_with_wrong_secret(
    client: TestClient, challenge_name: str
) -> None:
    response = client.post(
        "/submission", json={"challenge": challenge_name, "secret": "wrong_secret"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": False}


def test_invalid_json(client: TestClient) -> None:
    response = client.post("/submission", json={"invalid": "data"})
    assert response.status_code == 422  # FastAPI validation error
