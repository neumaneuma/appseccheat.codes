import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.helper import (
    allowed_to_continue_for_ssrf_challenge,
    get_ssrf_webhook_expected_response,
    timing_safe_compare,
)
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/ssrf1")

TIMEOUT = 0.25


class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_webhook/", response_model=str)
async def submit_webhook(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    if should_reveal_first_hint(user_supplied_url.url):
        return FIRST_HINT
    if should_reveal_second_hint(user_supplied_url.url):
        return SECOND_HINT
    if should_reveal_third_hint(user_supplied_url.url):
        return THIRD_HINT

    if not await allowed_to_continue_for_ssrf_challenge(
        user_supplied_url.url, is_valid_internal_url
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
        )

    try:
        r = requests.post(user_supplied_url.url, timeout=TIMEOUT)
        response_body = r.json()

        if timing_safe_compare(response_body, get_ssrf_webhook_expected_response()):
            return Passphrases.ssrf1.value
        else:
            raise HTTPException(
                status_code=400, detail=f"{response_body}...\n\nFailure"
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Failure: " + str(e)) from e


FIRST_HINT = "Docker container in use - use internal_api as hostname to access admin functionality."
SECOND_HINT = "Incorrect port. Use 12302 instead."
THIRD_HINT = "Use the /reset_admin_password endpoint to reset the admin password!"

INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:12302
INTERNAL_API = INTERNAL_API_NO_PORT + ":12302"

# http://internal_api:12302/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:12302/reset_admin_password
INTERNAL_API_WITH_PATH = INTERNAL_API_WITH_SLASH + "reset_admin_password"

# http://internal_api:12302/reset_admin_password/
INTERNAL_API_WITH_PATH_AND_SLASH = INTERNAL_API_WITH_PATH + "/"


VALID_INTERNAL_URLS = [
    INTERNAL_API,
    INTERNAL_API_WITH_SLASH,
    INTERNAL_API_WITH_PATH,
    INTERNAL_API_WITH_PATH_AND_SLASH,
]


def should_reveal_first_hint(url: str) -> bool:
    return url.startswith("http://127.0.0.1") or url.startswith("http://localhost")


def should_reveal_second_hint(url: str) -> bool:
    return url.startswith(INTERNAL_API_NO_PORT) and not url.startswith(INTERNAL_API)


def should_reveal_third_hint(url: str) -> bool:
    return url.startswith(INTERNAL_API) and url not in {
        INTERNAL_API_WITH_PATH,
        INTERNAL_API_WITH_PATH_AND_SLASH,
    }


def is_valid_internal_url(url: str) -> bool:
    return url in VALID_INTERNAL_URLS


def did_access_internal_api(url: str) -> bool:
    return url == INTERNAL_API_WITH_SLASH
