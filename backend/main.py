from fastapi import FastAPI
from pydantic import BaseModel

from backend.helper import timing_safe_compare

from .passphrases import Passphrases

app = FastAPI()


class Flag(BaseModel):
    secret: str
    challenge: str


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, World from the backend!"}


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

    return {"result": timing_safe_compare(flag.secret, expected)}
