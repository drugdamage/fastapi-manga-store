# user schemas
from pydantic import BaseModel
from enum import Enum


# roles in the system
class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


# data from the registration form
class UserCreate(BaseModel):
    username: str
    password: str
    role: Role = Role.user


# user data without the password
class UserOut(BaseModel):
    id: int
    username: str
    role: Role


# how the user is stored in the database
class UserInDB(UserOut):
    hashed_password: str
