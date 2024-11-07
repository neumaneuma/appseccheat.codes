from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import User, get_db
from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.patches import PATCHES

router = APIRouter(prefix=f"/{PATCHES}/sqli1/")


class Credentials(BaseModel):
    username: str
    password: str


@router.post("login/", response_model=str)
async def login(credentials: Credentials) -> str:
    async with get_db() as _:
        user: User | None = User.get(username=credentials.username)
        if user and timing_safe_compare(str(user.password), credentials.password):
            return Passphrases.sqli1.value

    raise HTTPException(status_code=403, detail="Failure")
