from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import get_db
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/sqli1/")


class Credentials(BaseModel):
    username: str
    password: str


@router.post("login/", response_model=str)
async def login(credentials: Credentials) -> str:
    query = f"SELECT * FROM user WHERE username = '{credentials.username}' AND password = '{credentials.password}'"
    async with get_db() as db:
        result = await db.execute_sql(query)
        result = await result.fetchall()

    if not result:
        raise HTTPException(status_code=403, detail="Failure")

    return Passphrases.sqli1.value
