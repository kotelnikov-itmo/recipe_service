from typing import Union
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from auth.services import UserService
from auth.models import User
from conf import get_settings


# --- Security settings ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = get_settings().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 24 * 36000

# ---


def authenticate_user(db, username: str, password: str) -> Union[bool, User]:
    user: User = UserService(db).get_user(username=username)
    if not user:
        return False
    try:
        if not pwd_context.verify(password, user.hpass):
            return False
    except ValueError:
        return False
    return user


def create_access_token(payload: dict):
    """Create JWT token with payload"""
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_payload(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
