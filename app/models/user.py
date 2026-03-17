from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    user = "user"
    manager = "manger"
    admin = "admin"


class UserCreate(BaseModel):
    username: str
    password: str
    role: Role = Role.user


class UserOut(BaseModel):
    id: int 
    username: str
    role: Role


class UserInDB(UserOut):
    hashed_password: str