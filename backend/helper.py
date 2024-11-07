import hmac
from collections.abc import Callable

import safehttpx
from peewee import CharField


def timing_safe_compare(a: str | CharField, b: str | CharField) -> bool:
    """Compare secrets using hmac.compare_digest to prevent timing analysis"""
    if isinstance(a, CharField):
        a = str(a)
    if isinstance(b, CharField):
        b = str(b)
    return hmac.compare_digest(a.encode(), b.encode())


async def allowed_to_continue_for_ssrf_challenge(
    url: str, check_valid_internal_urls: Callable[[str], bool]
) -> bool:
    if safehttpx.is_public_ip(url):
        return True

    for ip in await safehttpx.async_resolve_hostname_google(url):
        if safehttpx.is_public_ip(ip):
            return True

    return check_valid_internal_urls(url)
