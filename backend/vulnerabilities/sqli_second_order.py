import secrets

import bcrypt
from fastapi import APIRouter, HTTPException, Request
from peewee import DoesNotExist
from pydantic import BaseModel

from backend.constants import SESSION_IDENTIFIER
from backend.database import SQLI2_USERNAME, Session, User, db, deserialize_user
from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.vulnerabilities import VULNERABILITIES

router = APIRouter(prefix=f"/{VULNERABILITIES}/sqli2")


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

    with db:
        user = User.create(
            username=credentials.username,
            password=bcrypt.hashpw(credentials.password.encode(), bcrypt.gensalt()),
        )
        session: Session = Session.create(cookie=secrets.token_hex(), user=user)
        request.session[SESSION_IDENTIFIER] = session.cookie
    return "Successfully registered"


@router.post("/change_password/", response_model=str)
async def change_password(request: Request, change_password: ChangePassword) -> str:
    print("$$$ 1")
    if SESSION_IDENTIFIER not in request.session:
        raise HTTPException(status_code=403, detail="Unauthorized")

    print("$$$ 2")
    if len(change_password.old.strip()) == 0 or len(change_password.new.strip()) == 0:
        raise HTTPException(status_code=400, detail="Fields cannot be empty")

    print("$$$ 3")
    if change_password.new != change_password.new_verify:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    print("$$$ 4")
    cookie = request.session[SESSION_IDENTIFIER]
    print(f"$$$ 4a request.session: {request.session}")
    try:
        with db:
            session = Session.get(cookie=cookie)
    except DoesNotExist as err:
        raise HTTPException(status_code=403, detail="Unauthorized") from err

    print("$$$ 5")
    query = f"UPDATE appsec_cheat_codes_user SET password = '{change_password.new}' WHERE username = '{session.user.username}' AND password = '{change_password.old}'"
    with db:
        db.execute_sql(query)
        print("$$$ 6")
        hacked_user = deserialize_user(User.get(username=SQLI2_USERNAME))
    print("$$$ 7")
    if hacked_user is None:
        raise ValueError("Database is not properly initialized")
    print("$$$ 8")
    if timing_safe_compare(hacked_user.password, change_password.new):
        return Passphrases.sqli2.value

    return "Successfully changed password"
