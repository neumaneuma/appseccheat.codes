import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import db, deserialize_user
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/sqli1")
LOG = logging.getLogger(__name__)


class Credentials(BaseModel):
    username: str
    password: str


@router.post("/login/", response_model=str)
async def login(credentials: Credentials) -> str:
    query = f"SELECT * FROM appsec_cheat_codes_user WHERE username = '{credentials.username}' AND password = '{credentials.password}'"
    with db:
        result = db.execute_sql(query).fetchone()
    user = deserialize_user(result)
    if user:
        return Passphrases.sqli1.value

    raise HTTPException(status_code=403, detail="Failure")
