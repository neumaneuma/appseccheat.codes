import logging

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend import local_file_adapter
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/ssrf2/")
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25


class UserSuppliedUrl(BaseModel):
    url: str


@router.post("submit_api_url/", response_model=str)
async def submit_api_url(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    LOG.debug(f"User supplied URL: {user_supplied_url.url}")
    if should_reveal_first_hint(user_supplied_url.url):
        return FIRST_HINT

    if not is_valid_internal_url(user_supplied_url.url):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
        )

    try:
        requests_session = requests.session()
        requests_session.mount(FILE_SCHEME, local_file_adapter.LocalFileAdapter())
        r = requests_session.get(user_supplied_url.url, timeout=TIMEOUT)
        response_body = r.text[:1000]

        if did_successfully_get_file(user_supplied_url.url):
            return Passphrases.ssrf2.value
        elif accessed_cat_coin_api(user_supplied_url.url):
            return response_body
        else:
            raise HTTPException(
                status_code=400, detail=f"{response_body}...\n\nFailure"
            )
    except requests.exceptions.RequestException as e:
        LOG.debug("Request exception: " + str(e))
        raise HTTPException(status_code=400, detail="Failure: " + str(e)) from e


FILE_SCHEME = "file://"
ALLOWED_PATHS = [f"{FILE_SCHEME}/etc/passwd", f"{FILE_SCHEME}/etc/shadow"]
FIRST_HINT = "The scheme is correct, but that is not the right file"


INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:12301
INTERNAL_API = INTERNAL_API_NO_PORT + ":12301"

# http://internal_api:12301/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:12301/get_cat_coin_price_v1
INTERNAL_API_WITH_PATH_V1 = INTERNAL_API_WITH_SLASH + "get_cat_coin_price_v1"

# http://internal_api:12301/get_cat_coin_price_v2
INTERNAL_API_WITH_PATH_V2 = INTERNAL_API_WITH_SLASH + "get_cat_coin_price_v2"

# http://internal_api:12301/get_cat_coin_price_v1/
INTERNAL_API_WITH_PATH_AND_SLASH_V1 = INTERNAL_API_WITH_PATH_V1 + "/"

# http://internal_api:12301/get_cat_coin_price_v2/
INTERNAL_API_WITH_PATH_AND_SLASH_V2 = INTERNAL_API_WITH_PATH_V2 + "/"

VALID_INTERNAL_URLS = [
    INTERNAL_API,
    INTERNAL_API_WITH_SLASH,
    INTERNAL_API_WITH_PATH_V1,
    INTERNAL_API_WITH_PATH_AND_SLASH_V1,
    INTERNAL_API_WITH_PATH_V2,
    INTERNAL_API_WITH_PATH_AND_SLASH_V2,
]


def should_reveal_first_hint(url: str) -> bool:
    return url.startswith(FILE_SCHEME) and url not in ALLOWED_PATHS


def is_valid_internal_url(url: str) -> bool:
    return url in VALID_INTERNAL_URLS or url in ALLOWED_PATHS


def did_successfully_get_file(url: str) -> bool:
    return url in ALLOWED_PATHS


def accessed_cat_coin_api(url: str) -> bool:
    return url in VALID_INTERNAL_URLS
