import hmac
import ipaddress
from collections.abc import Callable
from urllib.parse import urlparse

import dns.resolver
from peewee import CharField


def timing_safe_compare(a: str | CharField, b: str | CharField) -> bool:
    """Compare secrets using hmac.compare_digest to prevent timing analysis"""
    if isinstance(a, CharField):
        a = str(a)
    if isinstance(b, CharField):
        b = str(b)
    return hmac.compare_digest(a.encode(), b.encode())


def is_public_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return not (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
        )
    except ValueError:
        return False


def allowed_to_continue_for_ssrf_challenge(
    url: str, check_valid_internal_urls: Callable[[str], bool] | None = None
) -> bool:
    if is_public_ip(url):
        return True

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.split(":")[0]  # Remove port if present

        answers = dns.resolver.resolve(hostname, "A")
        ips = {str(answer) for answer in answers}  # Use set to remove duplicates

        for ip in ips:
            if is_public_ip(ip):
                return True
    except Exception as e:
        print(f"Error resolving hostname: {e}")
        return False

    return check_valid_internal_urls(url) if check_valid_internal_urls else False


def get_ssrf_webhook_expected_response() -> str:
    # hard-coded copy from internal_api.main.simulate_reset_admin_password
    PASSWORD_RESET = (
        "E0304F61-0E09-4200-8086-AC2C6546F56F-835A6D48-E659-4F55-8730-9636A9F55E92"
    )
    return f"Administrator password reset to: {PASSWORD_RESET}"
