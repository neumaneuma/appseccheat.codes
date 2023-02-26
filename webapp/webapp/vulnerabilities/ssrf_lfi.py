import logging

import requests
from flask import Blueprint, request

from .. import local_file_adapter, secrets
from . import VULNERABILITIES_PREFIX, ssrf_helper

bp = Blueprint(
    "vulnerabilities_ssrf2", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/ssrf2"
)
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25


@bp.route("/submit_api_url/", methods=["POST"])
def submit_api_url():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 400)

    LOG.debug(f"User supplied URL: {custom_url}")
    if should_reveal_first_hint(custom_url):
        return (FIRST_HINT, 202)
    if not ssrf_helper.is_url_valid(custom_url, is_valid_internal_url):
        return (f"Failure: supplied url is invalid ({custom_url})", 400)

    try:
        requests_session = requests.session()
        requests_session.mount(
            'file://', local_file_adapter.LocalFileAdapter())
        r = requests_session.get(custom_url, timeout=TIMEOUT)
        response_body = r.text[:1000]

        if did_successfully_get_file(custom_url):
            return (
                f"{response_body}\n\nSuccess - passphrase: {secrets.PASSPHRASE['ssrf2']}",
                200,
            )
        elif accessed_cat_coin_api(custom_url):
            return (f"{response_body}", 200)
        else:
            return (f"{response_body}...\n\nFailure", 400)
    except requests.exceptions.RequestException as e:
        LOG.debug("Request exception: " + str(e))
        return ("Failure: " + str(e), 400)


FILE_SCHEME = "file://"
ALLOWED_URLS = [f"{FILE_SCHEME}/etc/passwd", f"{FILE_SCHEME}/etc/shadow"]
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


def should_reveal_first_hint(url):
    return url.startswith(FILE_SCHEME) and url not in ALLOWED_URLS


def is_valid_internal_url(url):
    return url in VALID_INTERNAL_URLS or url in ALLOWED_URLS


def did_successfully_get_file(url):
    return url in ALLOWED_URLS


def accessed_cat_coin_api(url):
    return url in VALID_INTERNAL_URLS
