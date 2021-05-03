import logging
from urllib.parse import urlparse
import ipaddress

import requests
from flask import Blueprint, request
import dns.message
import dns.query
import dns.rdatatype

from .. import secrets
from .. import local_file_adapter
from . import VULNERABILITIES_PREFIX

bp = Blueprint(
    "vulnerabilities_ssrf2", __name__, url_prefix=f"{VULNERABILITIES_PREFIX}/ssrf2"
)
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25
DNS_RESOLVER = "1.1.1.1"
# DNS_RESOLVER = "8.8.8.8"
# DNS_RESOLVER = "9.9.9.9"


@bp.route("/submit_api_url/", methods=["POST"])
def submit_api_url():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 400)

    LOG.debug(f"User supplied URL: {custom_url}")
    if should_reveal_first_hint(custom_url):
        return (FIRST_HINT, 202)
    if not is_url_valid(custom_url):
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


FILE_SCHEMA = "file://"
ALLOWED_URLS = [f"{FILE_SCHEMA}/etc/passwd", f"{FILE_SCHEMA}/etc/shadow"]


FIRST_HINT = "The schema is correct, but that is not the right file"


def should_reveal_first_hint(url):
    return url.startswith(FILE_SCHEMA) and url not in ALLOWED_URLS


def get_ip_address_from_dns(qname):
    try:
        q = dns.message.make_query(qname, dns.rdatatype.A)
        r = dns.query.tls(q, DNS_RESOLVER, timeout=TIMEOUT)
        if len(r.answer) > 0:
            return str(r.answer[0][0])
    except Exception as e:
        LOG.debug("Original address: " + qname)
        LOG.debug(e)
    return qname


def attempt_ip_address_parse(address):
    try:
        ip_addr = ipaddress.ip_address(address)
        return ip_addr
    except ValueError:
        return None


def is_invalid_scheme(scheme):
    return not (scheme == "https" or scheme == "http" or scheme == "")


INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:8484
INTERNAL_API = INTERNAL_API_NO_PORT + ":8484"

# http://internal_api:8484/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:8484/get_cat_coin_price
INTERNAL_API_WITH_PATH = INTERNAL_API_WITH_SLASH + "get_cat_coin_price"

# http://internal_api:8484/get_cat_coin_price/
INTERNAL_API_WITH_PATH_AND_SLASH = INTERNAL_API_WITH_PATH + "/"


def is_valid_internal_url(url):
    valid_internal_urls = [
        INTERNAL_API,
        INTERNAL_API_WITH_SLASH,
        INTERNAL_API_WITH_PATH,
        INTERNAL_API_WITH_PATH_AND_SLASH,
    ]
    return url in (valid_internal_urls + ALLOWED_URLS)


def is_url_valid(url):
    if is_valid_internal_url(url):
        LOG.debug(f"Valid internal url: {url}")
        return True

    # Attempt to see if url is a valid ip address first in order to avoid performing a dns look up if possible
    ip = attempt_ip_address_parse(url)
    if ip != None:
        is_global = ip.is_global
        LOG.debug(
            f"IP address successfully parsed on first attempt: {ip}. Returning {is_global} for is url valid"
        )
        return is_global

    parsed_url = urlparse(url)
    if is_invalid_scheme(parsed_url.scheme):
        LOG.debug(f"Invalid schema: {parsed_url.scheme}")
        return False

    # If urlparse is unable to correctly parse the url, then everything will be in the path
    hostname = parsed_url.hostname if parsed_url.hostname != None else parsed_url.path
    dns_ip = get_ip_address_from_dns(hostname)
    LOG.debug(f"Response from DNS: {dns_ip}")

    ip = attempt_ip_address_parse(dns_ip)
    if ip == None:
        LOG.debug("Unable to parse the IP address from the DNS response")
        return False

    is_global = ip.is_global
    LOG.debug(
        f"Returning {is_global} for is url valid. Is private: {ip.is_private}")
    return is_global


def did_successfully_get_file(url):
    return url in ALLOWED_URLS


def accessed_cat_coin_api(url):
    return url == INTERNAL_API_WITH_SLASH or url == INTERNAL_API_WITH_PATH_AND_SLASH
