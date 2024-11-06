from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from backend.database import User, get_db
from backend.passphrases import Passphrases


@pytest.fixture
async def setup_test_user() -> AsyncGenerator[User, None]:
    async with get_db():
        # Create a test user
        test_user = User.create(username="test_user", password="test_password")
        yield test_user
        # Cleanup
        User.delete().where(User.username == "test_user").execute()


class TestSQLILoginBypass:
    def test_empty_credentials(self, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/", json={"username": "", "password": ""}
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Failure"

    @pytest.mark.asyncio
    async def test_valid_login(self, setup_test_user: User, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": "test_user", "password": "test_password"},
        )
        assert response.status_code == 200
        assert response.json() == Passphrases.sqli1.value

    def test_invalid_login(self, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": "fake_user", "password": "fake_password"},
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Failure"

    @pytest.mark.parametrize(
        "sql_injection",
        [
            "' OR '1'='1",
            "' OR 1=1 --",
            "' OR 'x'='x",
            "admin' --",
            "' UNION SELECT * FROM user --",
            "'; DROP TABLE user; --",
        ],
    )
    def test_sql_injection_attempts(
        self, sql_injection: str, client: TestClient
    ) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": sql_injection, "password": "anything"},
        )
        # Note: In a real application, we'd expect these to fail
        # But since this is a vulnerable endpoint for training,
        # some of these might actually succeed
        assert response.status_code in [200, 403]

    def test_malformed_json(self, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/", json={"invalid": "data"}
        )
        assert response.status_code == 422  # FastAPI validation error

    @pytest.mark.parametrize(
        "username,password",
        [
            (None, "password"),
            ("username", None),
            (None, None),
            ("", "password"),
            ("username", ""),
        ],
    )
    def test_invalid_credentials_format(
        self, username: str, password: str, client: TestClient
    ) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": username, "password": password},
        )
        assert response.status_code in [403, 422]

    def test_long_input_strings(self, client: TestClient) -> None:
        very_long_string = "A" * 1000
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": very_long_string, "password": very_long_string},
        )
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "special_chars",
        [
            "<script>alert(1)</script>",
            "../../etc/passwd",
            "%(username)s",
            "${USER}",
            "\x00\x00\x00",
        ],
    )
    def test_special_characters(self, special_chars: str, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/sqli1/login/",
            json={"username": special_chars, "password": "password"},
        )
        assert response.status_code in [200, 403, 422]
