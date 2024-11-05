import logging

import requests
import safehttpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.helper import allowed_to_continue_for_ssrf_challenge, timing_safe_compare
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES
from ssrf.internal_api.admin_panel import simulate_reset_admin_password

router = APIRouter(prefix=f"/{VULNERABILITIES}/ssrf1/")
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25


class UserSuppliedUrl(BaseModel):
    url: str


@router.post("submit_webhook/", response_model=str)
async def submit_webhook(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    LOG.debug(f"User supplied URL: {user_supplied_url.url}")
    if should_reveal_first_hint(user_supplied_url.url):
        return FIRST_HINT
    if should_reveal_second_hint(user_supplied_url.url):
        return SECOND_HINT

    if not await allowed_to_continue_for_ssrf_challenge(
        user_supplied_url.url, is_valid_internal_url
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
        )

    try:
        r = safehttpx.get(user_supplied_url.url, timeout=TIMEOUT)
        response_body = r.text[:1000]

        if timing_safe_compare(response_body, simulate_reset_admin_password()):
            return Passphrases.ssrf1.value
        elif did_access_internal_api(user_supplied_url.url):
            return response_body
        else:
            raise HTTPException(
                status_code=400, detail=f"{response_body}...\n\nFailure"
            )
    except requests.exceptions.RequestException as e:
        LOG.debug("Request exception: " + str(e))
        raise HTTPException(status_code=400, detail="Failure: " + str(e)) from e


FIRST_HINT = "Docker container in use - use internal_api as hostname to access admin functionality."
SECOND_HINT = "Incorrect port. Use 12301 instead."

INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:12301
INTERNAL_API = INTERNAL_API_NO_PORT + ":12301"

# http://internal_api:12301/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:12301/reset_admin_password
INTERNAL_API_WITH_PATH = INTERNAL_API_WITH_SLASH + "reset_admin_password"

# http://internal_api:12301/reset_admin_password/
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


def is_valid_internal_url(url: str) -> bool:
    return url in VALID_INTERNAL_URLS


def did_successfully_reset_admin_password(url: str) -> bool:
    return url == INTERNAL_API_WITH_PATH or url == INTERNAL_API_WITH_PATH_AND_SLASH


def did_access_internal_api(url: str) -> bool:
    return url == INTERNAL_API_WITH_SLASH
