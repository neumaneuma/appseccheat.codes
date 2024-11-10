from fastapi import APIRouter, HTTPException
from peewee import DoesNotExist
from pydantic import BaseModel

from backend.database import User, db
from backend.passphrases import Passphrases
from backend.patches import PATCHES

router = APIRouter(prefix=f"/{PATCHES}/sqli1")


class Credentials(BaseModel):
    username: str
    password: str


@router.post("/login/", response_model=str)
async def login(credentials: Credentials) -> str:
    try:
        with db:
            User.get(username=credentials.username, password=credentials.password)
    except DoesNotExist as err:
        raise HTTPException(status_code=403, detail="Failure") from err
    else:
        return Passphrases.sqli1.value
