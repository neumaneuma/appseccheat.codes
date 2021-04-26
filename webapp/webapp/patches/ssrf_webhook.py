import logging
from urllib.parse import urlparse
import ipaddress

import requests
from flask import Blueprint, request
import dns.message
import dns.query
import dns.rdatatype

from .. import secrets
from . import PATCHES_PREFIX

bp = Blueprint(
    "patches_ssrf1", __name__, url_prefix=f"{PATCHES_PREFIX}/ssrf1"
)
LOG = logging.getLogger(__name__)

TIMEOUT = .25
DNS_RESOLVER = "1.1.1.1"
# DNS_RESOLVER = "8.8.8.8"
# DNS_RESOLVER = "9.9.9.9"


@bp.route("/submit_webhook/", methods=["POST"])
def submit_webhook():
    custom_url = request.form.get("custom_url")
    if not custom_url:
        return ("Failure: fields can not be empty", 401)

    LOG.debug(f"User supplied URL: {custom_url}")
    if is_url_invalid(custom_url):
        return (f"Failure: supplied url is invalid ({custom_url})", 401)

    try:
        r = requests.post(custom_url)
        response_body = r.text[:1000]

        return (
            (f"{response_body}\n\nSuccess - passphrase: {secrets.PASSPHRASE['ssrf1']}", 200)
            if was_successful_ssrf_attack(custom_url)
            else (f"{response_body}...\n\nFailure", 401)
        )
    except requests.exceptions.MissingSchema as e:
        return ("Failure: " + str(e), 401)


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


ADMIN_PANEL_NO_PORT = "http://admin_panel"

# http://admin_panel:8484
ADMIN_PANEL = ADMIN_PANEL_NO_PORT + ":8484"

# http://admin_panel:8484/
ADMIN_PANEL_WITH_SLASH = ADMIN_PANEL + "/"

# http://admin_panel:8484/reset_admin_password
ADMIN_PANEL_WITH_PATH = ADMIN_PANEL_WITH_SLASH + "reset_admin_password"

# http://admin_panel:8484/reset_admin_password/
ADMIN_PANEL_WITH_PATH_AND_SLASH = ADMIN_PANEL_WITH_PATH + "/"


def is_url_invalid(url):
    # Attempt to see if url is a valid ip address first in order to avoid performing a dns look up if possible
    ip = attempt_ip_address_parse(url)
    if ip != None:
        LOG.debug(f"IP address successfully parsed on first attempt: {ip}")
        return ip.is_private

    parsed_url = urlparse(url)
    if is_invalid_scheme(parsed_url.scheme):
        LOG.debug(f"Invalid schema: {parsed_url.scheme}")
        return True

    # If urlparse is unable to correctly parse the url, then everything will be in the path
    hostname = parsed_url.hostname if parsed_url.hostname != None else parsed_url.path
    dns_ip = get_ip_address_from_dns(hostname)
    LOG.debug(f"Response from DNS: {dns_ip}")

    ip = attempt_ip_address_parse(dns_ip)
    if ip == None:
        return True
    return ip.is_private


def was_successful_ssrf_attack(url):
    return url == ADMIN_PANEL_WITH_PATH or url == ADMIN_PANEL_WITH_PATH_AND_SLASH
