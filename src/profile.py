from typing import Annotated

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel


app = FastAPI()


class Profile(BaseModel):
    email: str = None
    phone: str = None


class UserDto(BaseModel):
    email: str = None
    phone: str = None


profiles: dict[str, Profile] = {}


def check_permission(login: str, x_auth_user: Annotated[str | None, Header()] = None):
    if login != x_auth_user:
        raise HTTPException(status_code=403)


@app.get(path='/users/{login}', dependencies=[Depends(check_permission)])
def get_user(login: str):
    if login not in profiles:
        profiles[login] = Profile()
    return profiles[login]


@app.post(path='/users/{login}', dependencies=[Depends(check_permission)])
def update_user(login: str, data: UserDto):
    if login not in profiles:
        profiles[login] = Profile()
    profile = profiles[login]
    profile.email = data.email
    profile.phone = data.phone

    return profile

