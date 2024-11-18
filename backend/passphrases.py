import secrets
from enum import Enum


class Passphrases(Enum):
    sqli1 = secrets.token_hex()
    sqli2 = secrets.token_hex()
    ssrf1 = secrets.token_hex()
    ssrf2 = secrets.token_hex()
