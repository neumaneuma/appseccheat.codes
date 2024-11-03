from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import get_db
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/")


class Login(BaseModel):
    username: str
    password: str


@router.post("sqli1/login/")
async def login(login: Login) -> str:
    if not len(login.username) or not len(login.password):
        raise HTTPException(status_code=400, detail="Fields can not be empty")

    query = f"SELECT * FROM sqli1_users WHERE password = '{login.password}' AND username = '{login.username}'"
    async with get_db() as db:
        result = await db.execute_sql(query)
        result = await result.fetchall()

    if not result:
        raise HTTPException(status_code=403, detail="Failure")

    return Passphrases.sqli1.value
