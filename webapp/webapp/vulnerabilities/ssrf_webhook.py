import logging

import requests
from flask import Blueprint, request

from .. import secrets
from . import VULNERABILITIES_PREFIX
from . import ssrf_helper

bp = Blueprint(
    "vulnerabilities_ssrf1", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/ssrf1"
)
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25


@bp.route("/submit_webhook/", methods=["POST"])
def submit_webhook():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 400)

    LOG.debug(f"User supplied URL: {custom_url}")
    if should_reveal_first_hint(custom_url):
        return (FIRST_HINT, 202)
    if should_reveal_second_hint(custom_url):
        return (SECOND_HINT, 202)
    if not ssrf_helper.is_url_valid(custom_url, is_valid_internal_url):
        return (f"Failure: supplied url is invalid ({custom_url})", 400)

    try:
        r = requests.post(custom_url, timeout=TIMEOUT)
        response_body = r.text[:1000]

        if did_successfully_reset_admin_password(custom_url):
            return (
                f"{response_body}\n\nSuccess - passphrase: {secrets.PASSPHRASE['ssrf1']}",
                200,
            )
        elif did_access_internal_api(custom_url):
            return (f"{response_body}", 200)
        else:
            return (f"{response_body}...\n\nFailure", 400)
    except requests.exceptions.RequestException as e:
        LOG.debug("Request exception: " + str(e))
        return ("Failure: " + str(e), 400)


FIRST_HINT = "Docker container in use - use internal_api as hostname to access admin functionality."
SECOND_HINT = "Incorrect port. Use 8484 instead."

INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:8484
INTERNAL_API = INTERNAL_API_NO_PORT + ":8484"

# http://internal_api:8484/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:8484/reset_admin_password
INTERNAL_API_WITH_PATH = INTERNAL_API_WITH_SLASH + "reset_admin_password"

# http://internal_api:8484/reset_admin_password/
INTERNAL_API_WITH_PATH_AND_SLASH = INTERNAL_API_WITH_PATH + "/"


VALID_INTERNAL_URLS = [
    INTERNAL_API,
    INTERNAL_API_WITH_SLASH,
    INTERNAL_API_WITH_PATH,
    INTERNAL_API_WITH_PATH_AND_SLASH,
]


def should_reveal_first_hint(url):
    return url.startswith("http://127.0.0.1") or url.startswith("http://localhost")


def should_reveal_second_hint(url):
    return url.startswith(INTERNAL_API_NO_PORT) and not url.startswith(INTERNAL_API)


def is_valid_internal_url(url):
    return url in VALID_INTERNAL_URLS


def did_successfully_reset_admin_password(url):
    return url == INTERNAL_API_WITH_PATH or url == INTERNAL_API_WITH_PATH_AND_SLASH


def did_access_internal_api(url):
    return url == INTERNAL_API_WITH_SLASH
