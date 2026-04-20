# сервис для входа и ролей
import hashlib
import os
import secrets

# ошибки и типы запросов
from fastapi import HTTPException, Request, status
from sqlalchemy import select

# подключаем базу и модель пользователя
from app.db import get_session
from app.models.database import UserDB
from app.models.user import Role

# уровни ролей для проверок
ROLE_LEVELS = {
    Role.user.value: 1,
    Role.manager.value: 2,
    Role.admin.value: 3,
}


def hash_password(password: str) -> str:
    # Делаем хеш пароля с солью.
    # генерируем случайную соль
    salt = os.urandom(16)
    # считаем хеш пароля
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"{salt.hex()}:{hashed.hex()}"


def verify_password(password: str, stored_value: str) -> bool:
    # Сравниваем пароль с хешем.
    # делим сохраненный текст на соль и хеш
    salt_hex, hash_hex = stored_value.split(":")
    salt = bytes.fromhex(salt_hex)
    # считаем хеш для нового ввода
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return secrets.compare_digest(hashed.hex(), hash_hex)


def create_user(username: str, password: str, role: str = Role.user.value) -> UserDB:
    # Создаем пользователя в базе.
    with get_session() as session:
        # ищем логин в таблице
        existing_user = session.scalar(select(UserDB).where(UserDB.username == username))
        if existing_user is not None:
            raise ValueError("User already exists")

        # собираем объект пользователя
        user = UserDB(
            username=username,
            password_hash=hash_password(password),
            role=role,
        )
        # добавляем пользователя в сессию
        session.add(user)
        # сохраняем изменения
        session.commit()
        # обновляем объект после commit
        session.refresh(user)
        return user


def authenticate_user(username: str, password: str) -> UserDB | None:
    # Проверяем логин и пароль.
    with get_session() as session:
        # ищем пользователя по логину
        user = session.scalar(select(UserDB).where(UserDB.username == username))
        if user is None:
            return None
        # проверяем пароль
        if not verify_password(password, user.password_hash):
            return None
        return user


def get_user_by_id(user_id: int) -> UserDB | None:
    # Ищем пользователя по id.
    with get_session() as session:
        # берем пользователя по первичному ключу
        user = session.get(UserDB, user_id)
        if user is None:
            return None
        return user


def get_all_users() -> list[UserDB]:
    # Берем всех пользователей.
    with get_session() as session:
        # сортируем по id
        users = session.scalars(select(UserDB).order_by(UserDB.id)).all()
        return users


def update_user_role(user_id: int, role: str) -> None:
    # Меняем роль пользователя.
    # сначала проверяем, что роль нормальная
    if role not in ROLE_LEVELS:
        raise ValueError("Role not found")

    with get_session() as session:
        # ищем пользователя в таблице
        user = session.get(UserDB, user_id)
        if user is None:
            raise ValueError("User not found")
        # меняем поле role
        user.role = role
        session.commit()


def get_current_user(request: Request) -> UserDB | None:
    # Берем пользователя из сессии.
    # читаем user_id из cookie сессии
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(user_id)


def login_user(request: Request, user: UserDB) -> None:
    # Сохраняем id пользователя в сессии.
    request.session["user_id"] = user.id


def logout_user(request: Request) -> None:
    # Чистим сессию при выходе.
    request.session.clear()


def require_login(request: Request) -> UserDB:
    # Проверяем, что пользователь вошел.
    user = get_current_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )
    return user


def has_role(user: UserDB, required_role: str) -> bool:
    # сравниваем уровни ролей
    return ROLE_LEVELS[user.role] >= ROLE_LEVELS[required_role]


def require_role(request: Request, required_role: str) -> UserDB:
    # Проверяем роль пользователя.
    user = require_login(request)
    if not has_role(user, required_role):
        raise HTTPException(status_code=403, detail="Forbidden")
    return user
