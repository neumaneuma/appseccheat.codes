import secrets

import bcrypt
from fastapi import APIRouter, HTTPException, Request
from peewee import DoesNotExist
from pydantic import BaseModel

from backend.database import SQLI2_USERNAME, Session, User, db, deserialize_user
from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/sqli2")

SESSION_IDENTIFIER = "sid"


class Credentials(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    old: str
    new: str
    new_verify: str


@router.post("/register/", response_model=str)
async def register(request: Request, credentials: Credentials) -> str:
    if len(credentials.username.strip()) == 0 or len(credentials.password.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    user = User.create(
        username=credentials.username,
        password=bcrypt.hashpw(credentials.password.encode(), bcrypt.gensalt()),
    )
    session = Session.create(cookie=secrets.token_hex(), user=user)
    request.session[SESSION_IDENTIFIER] = str(session.session_id)
    return "Successfully registered"


@router.post("/change_password/", response_model=str)
async def change_password(request: Request, change_password: ChangePassword) -> str:
    if SESSION_IDENTIFIER not in request.session:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if len(change_password.old.strip()) == 0 or len(change_password.new.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    if change_password.new != change_password.new_verify:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    cookie = request.session[SESSION_IDENTIFIER]
    try:
        cookie = Session.get(cookie=cookie)
    except DoesNotExist as err:
        raise HTTPException(status_code=403, detail="Unauthorized") from err

    query = f"UPDATE appsec_cheat_codes_user SET password = '{change_password.new}' WHERE username = '{cookie.user.username}' AND password = '{change_password.old}'"
    db.execute_sql(query)
    hacked_user = deserialize_user(User.get(username=SQLI2_USERNAME))
    if hacked_user is None:
        raise ValueError("Database is not properly initialized")
    if timing_safe_compare(hacked_user.password, change_password.new):
        return Passphrases.sqli2.value

    return "Successfully changed password"
