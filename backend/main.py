from fastapi import FastAPI
from pydantic import BaseModel

from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.patches.sqli_login_bypass import router as sqli_login_bypass_patched_router
from backend.patches.sqli_second_order import router as sqli_second_order_patched_router
from backend.patches.ssrf_lfi import router as ssrf_lfi_patched_router
from backend.patches.ssrf_webhook import router as ssrf_webhook_patched_router

# Import all modules with routes
from backend.vulnerabilities.sqli_login_bypass import (
    router as sqli_login_bypass_vulnerable_router,
)
from backend.vulnerabilities.sqli_second_order import (
    router as sqli_second_order_vulnerable_router,
)
from backend.vulnerabilities.ssrf_lfi import router as ssrf_lfi_vulnerable_router
from backend.vulnerabilities.ssrf_webhook import (
    router as ssrf_webhook_vulnerable_router,
)

app = FastAPI()

app.include_router(sqli_login_bypass_vulnerable_router)
app.include_router(sqli_second_order_vulnerable_router)
app.include_router(ssrf_webhook_vulnerable_router)
app.include_router(ssrf_lfi_vulnerable_router)
app.include_router(sqli_login_bypass_patched_router)
app.include_router(sqli_second_order_patched_router)
app.include_router(ssrf_webhook_patched_router)
app.include_router(ssrf_lfi_patched_router)


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
