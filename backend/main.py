from enum import Enum
import hmac
from typing import Union
from starlette import status
from fastapi import FastAPI, Response
from pydantic import BaseModel
import backend.local_flags as local_flags

app = FastAPI()

challenges = {"sqli-login-bypass", "sqli-second-order", "ssrf-bypass-webhook", "ssrf-local-file-inclusion"}

class SolutionBody(BaseModel):
    flag: str

@app.post("/flag/{challenge}")
def flag_submission(challenge: str, body: SolutionBody, response: Response) -> dict[str,str]:
    if challenge not in challenges:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Challenge not found"}
    
    if hmac.compare_digest(body.flag, local_flags.FLAGS[challenge]):
        response.status_code = status.HTTP_200_OK
        return {"message": "Challenge completed!"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Flag incorrect"}
    
class SQLiLoginBypassBody(BaseModel):
    username: str
    password: str

@app.post("/vulnerable/sqli-login-bypass")
def vulnerable_sqli_login_bypass(body: SQLiLoginBypassBody, response: Response) -> dict[str,str]:
    if body.username != 'administrator' or body.password == '':
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Login incorrect"}
    
    query = f"SELECT * FROM sqli-login-bypass_users WHERE password = '{body.password}' AND username = '{body.username}'"


