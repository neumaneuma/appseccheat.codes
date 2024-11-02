import ipaddress
import logging
from urllib.parse import urlparse

import dns.message
import dns.query
import dns.rdatatype

LOG = logging.getLogger(__name__)

TIMEOUT = 0.25
DNS_RESOLVER = "1.1.1.1"
# DNS_RESOLVER = "8.8.8.8"
# DNS_RESOLVER = "9.9.9.9"


# In order to simultaneously make this a valid ssrf vulnerability, but also not render my entire
# web app and cloud infrastructure vulnerable to ssrf, I had to finesse together an allowlist-blocklist
# mutant hybrid that could perform an ssrf attack on the input I allow, but prevent it for anything else.
def is_url_valid(url, is_valid_internal_url):
    if is_valid_internal_url(url):
        LOG.debug(f"Valid internal url: {url}")
        return True

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
