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


def get_ssrf_webhook_expected_response() -> str:
    # hard-coded copy from internal_api.main.simulate_reset_admin_password
    # TODO is there a better way to do this?
    PASSWORD_RESET = (
        "E0304F61-0E09-4200-8086-AC2C6546F56F-835A6D48-E659-4F55-8730-9636A9F55E92"
    )
    return f"Administrator password reset to: {PASSWORD_RESET}"
