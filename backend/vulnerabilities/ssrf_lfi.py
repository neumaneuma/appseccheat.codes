import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend import local_file_adapter
from backend.helper import allowed_to_continue_for_ssrf_challenge, timing_safe_compare
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/ssrf2")

TIMEOUT = 0.25


class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_api_url/", response_model=str)
async def submit_api_url(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    if should_reveal_first_hint(user_supplied_url.url):
        return FIRST_HINT

    if not allowed_to_continue_for_ssrf_challenge(
        user_supplied_url.url, is_valid_internal_url
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Failure: supplied url is invalid ({user_supplied_url.url})",
        )

    try:
        requests_session = requests.session()
        requests_session.mount(FILE_SCHEME, local_file_adapter.LocalFileAdapter())
        r = requests_session.get(user_supplied_url.url, timeout=TIMEOUT)
        response_body = r.text[:750].strip()
        print(f"$$$ 1 - {len(r.text.strip())}")

        # Read allowed files from disk
        passwd_contents = ""
        shadow_contents = ""

        try:
            with open("/etc/passwd") as f:
                passwd_contents = f.read().strip()
            with open("/etc/shadow") as f:
                shadow_contents = f.read().strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}") from e

        # Check if response matches either file
        if timing_safe_compare(response_body, passwd_contents) or timing_safe_compare(
            response_body, shadow_contents
        ):
            return Passphrases.ssrf2.value
        elif accessed_cat_coin_api(user_supplied_url.url):
            return response_body
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e


FILE_SCHEME = "file://"
ALLOWED_PATHS = {f"{FILE_SCHEME}/etc/passwd", f"{FILE_SCHEME}/etc/shadow"}
FIRST_HINT = "The scheme is correct, but that is not the right file."


INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:12302
INTERNAL_API = INTERNAL_API_NO_PORT + ":12302"

# http://internal_api:12302/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:12302/get_cat_coin_price_v1
INTERNAL_API_WITH_PATH_V1 = INTERNAL_API_WITH_SLASH + "get_cat_coin_price_v1"

# http://internal_api:12302/get_cat_coin_price_v2
INTERNAL_API_WITH_PATH_V2 = INTERNAL_API_WITH_SLASH + "get_cat_coin_price_v2"

# http://internal_api:12302/get_cat_coin_price_v1/
INTERNAL_API_WITH_PATH_AND_SLASH_V1 = INTERNAL_API_WITH_PATH_V1 + "/"

# http://internal_api:12302/get_cat_coin_price_v2/
INTERNAL_API_WITH_PATH_AND_SLASH_V2 = INTERNAL_API_WITH_PATH_V2 + "/"

VALID_INTERNAL_URLS = {
    INTERNAL_API,
    INTERNAL_API_WITH_SLASH,
    INTERNAL_API_WITH_PATH_V1,
    INTERNAL_API_WITH_PATH_AND_SLASH_V1,
    INTERNAL_API_WITH_PATH_V2,
    INTERNAL_API_WITH_PATH_AND_SLASH_V2,
}


def should_reveal_first_hint(url: str) -> bool:
    return url.startswith(FILE_SCHEME) and url not in ALLOWED_PATHS


def is_valid_internal_url(url: str) -> bool:
    return url in VALID_INTERNAL_URLS or url in ALLOWED_PATHS


def accessed_cat_coin_api(url: str) -> bool:
    return url in VALID_INTERNAL_URLS
