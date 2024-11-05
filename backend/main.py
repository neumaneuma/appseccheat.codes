import hmac

from fastapi import FastAPI
from passphrases import Passphrases
from pydantic import BaseModel

app = FastAPI()


class Flag(BaseModel):
    secret: str
    challenge: str


def timing_attack_safe_compare(a: str, b: str) -> bool:
    """
    Compare secrets using hmac.compare_digest to prevent timing attacks.
    """
    return hmac.compare_digest(a.encode(), b.encode())


@app.post("/submission")
async def submission(flag: Flag) -> dict[str, bool | str]:
    match flag.challenge:
        case Passphrases.sqli1.name:
            expected = Passphrases.sqli1.value
        case Passphrases.sqli2.name:
            expected = Passphrases.sqli2.value
        case Passphrases.ssrf1.name:
            expected = Passphrases.ssrf1.value
        case Passphrases.ssrf2.name:
            expected = Passphrases.ssrf2.value
        case _:
            return {"result": False, "message": "Invalid challenge"}

    return {"result": timing_attack_safe_compare(flag.secret, expected)}