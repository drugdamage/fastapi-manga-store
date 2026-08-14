# service for login and roles
import hashlib
import os
import secrets

# errors and request types
from fastapi import HTTPException, Request, status
from sqlalchemy import select

# wire up the database and user model
from app.db import get_session
from app.models.database import UserDB
from app.models.user import Role

# role levels for checks
ROLE_LEVELS = {
    Role.user.value: 1,
    Role.manager.value: 2,
    Role.admin.value: 3,
}


def hash_password(password: str) -> str:
    # Hash the password with a salt.
    # generate a random salt
    salt = os.urandom(16)
    # compute the password hash
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"{salt.hex()}:{hashed.hex()}"


def verify_password(password: str, stored_value: str) -> bool:
    # Compare the password against the hash.
    # split the stored value into salt and hash
    salt_hex, hash_hex = stored_value.split(":")
    salt = bytes.fromhex(salt_hex)
    # compute the hash for the new input
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return secrets.compare_digest(hashed.hex(), hash_hex)


def create_user(username: str, password: str, role: str = Role.user.value) -> UserDB:
    # Create the user in the database.
    with get_session() as session:
        # look up the username in the table
        existing_user = session.scalar(select(UserDB).where(UserDB.username == username))
        if existing_user is not None:
            raise ValueError("User already exists")

        # build the user object
        user = UserDB(
            username=username,
            password_hash=hash_password(password),
            role=role,
        )
        # add the user to the session
        session.add(user)
        # save changes
        session.commit()
        # refresh the object after commit
        session.refresh(user)
        return user


def authenticate_user(username: str, password: str) -> UserDB | None:
    # Check username and password.
    with get_session() as session:
        # look up the user by username
        user = session.scalar(select(UserDB).where(UserDB.username == username))
        if user is None:
            return None
        # check the password
        if not verify_password(password, user.password_hash):
            return None
        return user


def get_user_by_id(user_id: int) -> UserDB | None:
    # Look up the user by id.
    with get_session() as session:
        # get the user by primary key
        user = session.get(UserDB, user_id)
        if user is None:
            return None
        return user


def get_all_users() -> list[UserDB]:
    # Get all users.
    with get_session() as session:
        # sort by id
        users = session.scalars(select(UserDB).order_by(UserDB.id)).all()
        return users


def update_user_role(user_id: int, role: str) -> None:
    # Change the user's role.
    # first check the role is valid
    if role not in ROLE_LEVELS:
        raise ValueError("Role not found")

    with get_session() as session:
        # look up the user in the table
        user = session.get(UserDB, user_id)
        if user is None:
            raise ValueError("User not found")
        # update the role field
        user.role = role
        session.commit()


def get_current_user(request: Request) -> UserDB | None:
    # Get the user from the session.
    # read user_id from the session cookie
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(user_id)


def login_user(request: Request, user: UserDB) -> None:
    # Store the user id in the session.
    request.session["user_id"] = user.id


def logout_user(request: Request) -> None:
    # Clear the session on logout.
    request.session.clear()


def require_login(request: Request) -> UserDB:
    # Check that the user is logged in.
    user = get_current_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )
    return user


def has_role(user: UserDB, required_role: str) -> bool:
    # compare role levels
    return ROLE_LEVELS[user.role] >= ROLE_LEVELS[required_role]


def require_role(request: Request, required_role: str) -> UserDB:
    # Check the user's role.
    user = require_login(request)
    if not has_role(user, required_role):
        raise HTTPException(status_code=403, detail="Forbidden")
    return user
