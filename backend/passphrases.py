import os
import secrets
from enum import Enum


class Passphrases(Enum):
    sqli1 = "test_sqli1" if os.getenv("DEV_MODE") == "true" else secrets.token_hex()
    sqli2 = "test_sqli2" if os.getenv("DEV_MODE") == "true" else secrets.token_hex()
    ssrf1 = "test_ssrf1" if os.getenv("DEV_MODE") == "true" else secrets.token_hex()
    ssrf2 = "test_ssrf2" if os.getenv("DEV_MODE") == "true" else secrets.token_hex()
