from unittest.mock import Mock, patch

import requests
from fastapi.testclient import TestClient


def test_empty_url(client: TestClient) -> None:
    response = client.post("/vulnerabilities/ssrf2/submit_api_url/", json={"url": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Fields can not be empty"


def test_first_hint(client: TestClient) -> None:
    response = client.post(
        "/vulnerabilities/ssrf2/submit_api_url/", json={"url": "file:///wrong/path"}
    )
    assert response.status_code == 200
    assert response.json() == "The scheme is correct, but that is not the right file"


@patch("requests.session")
def test_valid_internal_url(mock_session: Mock, client: TestClient) -> None:
    mock_response = Mock()
    mock_response.text = "some response"
    mock_session.return_value.get.return_value = mock_response

    response = client.post(
        "/vulnerabilities/ssrf2/submit_api_url/",
        json={"url": "http://internal_api:12301/get_cat_coin_price_v1"},
    )
    assert response.status_code == 200


@patch("requests.session")
def test_timeout_error(mock_session: Mock, client: TestClient) -> None:
    mock_session.return_value.get.side_effect = requests.exceptions.Timeout()

    response = client.post(
        "/vulnerabilities/ssrf2/submit_api_url/",
        json={"url": "http://internal_api:12301"},
    )
    assert response.status_code == 400
    assert "Failure: " in response.json()["detail"]
