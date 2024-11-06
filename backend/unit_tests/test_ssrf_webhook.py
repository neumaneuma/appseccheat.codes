from unittest.mock import Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient

from backend.passphrases import Passphrases
from backend.vulnerabilities.ssrf_webhook import (
    FIRST_HINT,
    INTERNAL_API,
    INTERNAL_API_WITH_PATH,
    INTERNAL_API_WITH_PATH_AND_SLASH,
    INTERNAL_API_WITH_SLASH,
    SECOND_HINT,
)


class TestSubmitWebhook:
    @pytest.mark.parametrize("empty_url", ["", None])
    def test_empty_url(self, empty_url: str | None, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/", json={"url": empty_url}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Fields can not be empty"

    @pytest.mark.parametrize(
        "localhost_url",
        [
            "http://127.0.0.1",
            "http://127.0.0.1:8080",
            "http://localhost",
            "http://localhost:8080",
        ],
    )
    def test_first_hint_triggers(self, localhost_url: str, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/", json={"url": localhost_url}
        )
        assert response.status_code == 200
        assert response.json() == FIRST_HINT

    @pytest.mark.parametrize(
        "wrong_port_url",
        [
            "http://internal_api",
            "http://internal_api:8080",
            "http://internal_api:12300",
        ],
    )
    def test_second_hint_triggers(
        self, wrong_port_url: str, client: TestClient
    ) -> None:
        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/", json={"url": wrong_port_url}
        )
        assert response.status_code == 200
        assert response.json() == SECOND_HINT

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "http://evil.com",
            "https://internal_api:12301",
            "ftp://internal_api:12301",
            f"{INTERNAL_API}/invalid_path",
            "http://internal_api:12301/reset_admin_password_fake",
        ],
    )
    def test_invalid_urls_rejected(self, invalid_url: str, client: TestClient) -> None:
        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/", json={"url": invalid_url}
        )
        assert response.status_code == 400
        assert "Failure: supplied url is invalid" in response.json()["detail"]

    @pytest.mark.parametrize(
        "valid_url",
        [
            INTERNAL_API,
            INTERNAL_API_WITH_SLASH,
            INTERNAL_API_WITH_PATH,
            INTERNAL_API_WITH_PATH_AND_SLASH,
        ],
    )
    @patch("requests.post")
    def test_valid_urls_accepted(
        self, mock_post: Mock, valid_url: str, client: TestClient
    ) -> None:
        mock_response = Mock()
        mock_response.text = "test response"
        mock_post.return_value = mock_response

        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/", json={"url": valid_url}
        )
        assert response.status_code in [
            200,
            400,
        ]  # Depending on the URL, might be valid but fail the challenge
        mock_post.assert_called_once_with(valid_url, timeout=0.25)

    @patch("requests.post")
    def test_successful_admin_password_reset(
        self, mock_post: Mock, client: TestClient
    ) -> None:
        from ssrf.internal_api.main import simulate_reset_admin_password

        mock_response = Mock()
        mock_response.text = simulate_reset_admin_password()
        mock_post.return_value = mock_response

        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/",
            json={"url": INTERNAL_API_WITH_PATH},
        )
        assert response.status_code == 200
        assert response.json() == Passphrases.ssrf1.value

    @pytest.mark.parametrize(
        "exception_class",
        [
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
        ],
    )
    @patch("requests.post")
    def test_request_exceptions(
        self, mock_post: Mock, exception_class: type[Exception], client: TestClient
    ) -> None:
        mock_post.side_effect = exception_class("Test error")

        response = client.post(
            "/vulnerabilities/ssrf1/submit_webhook/",
            json={"url": INTERNAL_API_WITH_SLASH},
        )
        assert response.status_code == 400
        assert "Failure: " in response.json()["detail"]


class TestHelperFunctions:
    @pytest.mark.parametrize(
        "test_url,expected",
        [
            ("http://127.0.0.1", True),
            ("http://localhost", True),
            ("http://internal_api", False),
            ("http://evil.com", False),
        ],
    )
    def test_should_reveal_first_hint(
        self, test_url: str, expected: bool, client: TestClient
    ) -> None:
        from backend.vulnerabilities.ssrf_webhook import should_reveal_first_hint

        assert should_reveal_first_hint(test_url) == expected

    @pytest.mark.parametrize(
        "test_url,expected",
        [
            ("http://internal_api", True),
            ("http://internal_api:12301", False),
            ("http://internal_api:8080", True),
            ("http://evil.com", False),
        ],
    )
    def test_should_reveal_second_hint(
        self, test_url: str, expected: bool, client: TestClient
    ) -> None:
        from backend.vulnerabilities.ssrf_webhook import should_reveal_second_hint

        assert should_reveal_second_hint(test_url) == expected

    @pytest.mark.parametrize(
        "test_url,expected",
        [
            (INTERNAL_API, True),
            (INTERNAL_API_WITH_SLASH, True),
            (INTERNAL_API_WITH_PATH, True),
            (INTERNAL_API_WITH_PATH_AND_SLASH, True),
            ("http://evil.com", False),
            ("http://internal_api:12301/fake_path", False),
        ],
    )
    def test_is_valid_internal_url(
        self, test_url: str, expected: bool, client: TestClient
    ) -> None:
        from backend.vulnerabilities.ssrf_webhook import is_valid_internal_url

        assert is_valid_internal_url(test_url) == expected

    @pytest.mark.parametrize(
        "test_url,expected",
        [
            (INTERNAL_API_WITH_SLASH, True),
            (INTERNAL_API, False),
            (INTERNAL_API_WITH_PATH, False),
            ("http://evil.com", False),
        ],
    )
    def test_did_access_internal_api(
        self, test_url: str, expected: bool, client: TestClient
    ) -> None:
        from backend.vulnerabilities.ssrf_webhook import did_access_internal_api

        assert did_access_internal_api(test_url) == expected
