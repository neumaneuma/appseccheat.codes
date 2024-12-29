import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.helper import (
    allowed_to_continue_for_ssrf_challenge,
    get_ssrf_webhook_expected_response,
    timing_safe_compare,
)
from backend.passphrases import Passphrases
from backend.patches import PATCHES

router = APIRouter(prefix=f"/{PATCHES}/ssrf1")

TIMEOUT = 0.25


class UserSuppliedUrl(BaseModel):
    url: str


@router.post("/submit_webhook/", response_model=str)
async def submit_webhook(user_supplied_url: UserSuppliedUrl) -> str:
    if not user_supplied_url.url:
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    # Add scheme if missing
    url = (
        user_supplied_url.url
        if user_supplied_url.url.startswith(("http://", "https://"))
        else f"http://{user_supplied_url.url}"
    )

    if not allowed_to_continue_for_ssrf_challenge(url):
        raise HTTPException(
            status_code=400, detail=f"Failure: supplied url is invalid ({url})"
        )

    try:
        r = requests.post(url, timeout=TIMEOUT)
        try:
            response_body = r.json()
        except Exception:
            response_body = r.text[:750].strip()

        if timing_safe_compare(response_body, get_ssrf_webhook_expected_response()):
            return Passphrases.ssrf1.value
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Challenge failed. Response body: {response_body}",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failure: {e}") from e
