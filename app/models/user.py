# схемы пользователя
from pydantic import BaseModel
from enum import Enum


# роли в системе
class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


# данные из формы регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: Role = Role.user


# данные пользователя без пароля
class UserOut(BaseModel):
    id: int 
    username: str
    role: Role


# как пользователь хранится в базе
class UserInDB(UserOut):
    hashed_password: str
