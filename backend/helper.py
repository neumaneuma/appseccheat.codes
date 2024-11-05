import hmac


def timing_safe_compare(a: str, b: str) -> bool:
    """Compare secrets using hmac.compare_digest to prevent timing analysis"""
    return hmac.compare_digest(a.encode(), b.encode())
