from typing import Annotated

import hashlib
from uuid import uuid4
from fastapi import FastAPI, Response, HTTPException, Cookie
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    login: str
    hash: str


users: dict[str, User] = {}
sessions: dict[str, str] = {}


class UserDto(BaseModel):
    login: str
    password: str


@app.post(path='/registration')
def register_user(data: UserDto):
    users[data.login] = User(
        login=data.login,
        hash=hashlib.md5(data.password.encode()).hexdigest()
    )
    return {'success': True}


@app.post(path='/login')
def login_user(data: UserDto, response: Response):
    try:
        user = users[data.login]
    except KeyError:
        raise HTTPException(status_code=401)

    if not hashlib.md5(data.password.encode()).hexdigest() == user.hash:
        raise HTTPException(status_code=401)

    session_id = str(uuid4())
    sessions[session_id] = user.login
    response.set_cookie('session_id', session_id)


@app.post(path='/logout')
def logout_user(response: Response, session_id: Annotated[str | None, Cookie()] = None):
    if session_id is not None:
        sessions.pop(session_id)
        response.delete_cookie('session_id')


@app.api_route(path='/auth', methods=["GET", "POST"])
def auth_user(session_id: Annotated[str | None, Cookie()] = None):
    if session_id is None:
        raise HTTPException(status_code=401)
    try:
        login = sessions[session_id]
    except KeyError:
        raise HTTPException(status_code=401)

    return Response(
        headers={
            'x-auth-user': login
        }
    )

