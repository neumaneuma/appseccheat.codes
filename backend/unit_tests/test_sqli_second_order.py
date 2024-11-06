from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from backend.database import Session, User


@pytest.fixture
def cleanup_db() -> Generator[None, None, None]:
    yield
    User.delete().execute()
    Session.delete().execute()


def test_register_success(cleanup_db: None, client: TestClient) -> None:
    response = client.post(
        "/vulnerabilities/sqli2/register/",
        json={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    assert response.json() == "Successfully registered"
    assert "sid" in client.cookies


def test_register_empty_fields(client: TestClient) -> None:
    response = client.post(
        "/vulnerabilities/sqli2/register/", json={"username": "", "password": ""}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fields cannot be empty"


def test_change_password_unauthorized(client: TestClient) -> None:
    response = client.post(
        "/vulnerabilities/sqli2/change_password/",
        json={"old": "oldpass", "new": "newpass", "new_verify": "newpass"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Unauthorized"


def test_change_password_mismatch(cleanup_db: None, client: TestClient) -> None:
    # First register
    client.post(
        "/vulnerabilities/sqli2/register/",
        json={"username": "testuser", "password": "testpass"},
    )

    response = client.post(
        "/vulnerabilities/sqli2/change_password/",
        json={"old": "testpass", "new": "newpass", "new_verify": "different"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Passwords do not match"
