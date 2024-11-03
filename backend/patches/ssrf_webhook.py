import ipaddress
import logging
from urllib.parse import urlparse

import dns.message
import dns.query
import dns.rdatatype
import requests
from flask import Blueprint, request

from .. import secrets
from . import PATCHES_PREFIX

bp = Blueprint("patches_ssrf1", __name__, url_prefix=f"{PATCHES_PREFIX}/ssrf1")
LOG = logging.getLogger(__name__)

TIMEOUT = 0.25
DNS_RESOLVER = "1.1.1.1"
# DNS_RESOLVER = "8.8.8.8"
# DNS_RESOLVER = "9.9.9.9"


@bp.route("/submit_webhook/", methods=["POST"])
def submit_webhook():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 400)

    LOG.debug(f"User supplied URL: {custom_url}")
    if not input_is_permitted_through_blocklist(custom_url):
        return (f"Failure: supplied url is invalid ({custom_url})", 400)

    try:
        r = requests.post(custom_url, timeout=TIMEOUT)
        response_body = r.text[:1000]

        return (
            (
                f"{response_body}\n\nSuccess - passphrase: {secrets.PASSPHRASE['ssrf1']}",
                200,
            )
            if did_successfully_reset_admin_password(custom_url)
            else (f"{response_body}...\n\nFailure", 400)
        )
    except requests.exceptions.RequestException as e:
        LOG.debug("Request exception: " + str(e))
        return ("Failure: " + str(e), 400)


INTERNAL_API_NO_PORT = "http://internal_api"

# http://internal_api:12301
INTERNAL_API = INTERNAL_API_NO_PORT + ":12301"

# http://internal_api:12301/
INTERNAL_API_WITH_SLASH = INTERNAL_API + "/"

# http://internal_api:12301/reset_admin_password
INTERNAL_API_WITH_PATH = INTERNAL_API_WITH_SLASH + "reset_admin_password"

# http://internal_api:12301/reset_admin_password/
INTERNAL_API_WITH_PATH_AND_SLASH = INTERNAL_API_WITH_PATH + "/"


# This is what a blocklist implementation should look like
def input_is_permitted_through_blocklist(url):
    # Attempt to see if url is a valid ip address first in order to avoid performing a dns look up if possible
    ip = attempt_ip_address_parse(url)
    if ip is not None:
        is_global = ip.is_global
        LOG.debug(f"IP address successfully parsed on first attempt: {ip}. Returning {is_global} for is url valid")
        return is_global

    parsed_url = urlparse(url)
    if is_invalid_scheme(parsed_url.scheme):
        LOG.debug(f"Invalid schema: {parsed_url.scheme}")
        return False

    # If urlparse is unable to correctly parse the url, then everything will be in the path
    hostname = parsed_url.hostname if parsed_url.hostname is not None else parsed_url.path
    dns_ip = get_ip_address_from_dns(hostname)
    LOG.debug(f"Response from DNS: {dns_ip}")

    ip = attempt_ip_address_parse(dns_ip)
    if ip is None:
        LOG.debug("Unable to parse the IP address from the DNS response")
        return False

    is_global = ip.is_global
    LOG.debug(f"Returning {is_global} for is url valid. Is private: {ip.is_private}")
    return is_global


def attempt_ip_address_parse(address):
    try:
        ip_addr = ipaddress.ip_address(address)
        return ip_addr
    except ValueError:
        return None


def is_invalid_scheme(scheme):
    return not (scheme == "https" or scheme == "http" or scheme == "")


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


def did_successfully_reset_admin_password(url):
    return url == INTERNAL_API_WITH_PATH or url == INTERNAL_API_WITH_PATH_AND_SLASH
