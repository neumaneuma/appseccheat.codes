from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import User, get_db
from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/sqli1/")


class Credentials(BaseModel):
    username: str
    password: str


@router.post("login/", response_model=str)
async def login(credentials: Credentials) -> str:
    query = f"SELECT * FROM user WHERE username = '{credentials.username}'"
    async with get_db() as db:
        result = await db.execute_sql(query)
        user: User | None = await result.fetchall()
        if user and timing_safe_compare(user.password, credentials.password):
            return Passphrases.sqli1.value

    raise HTTPException(status_code=403, detail="Failure")
