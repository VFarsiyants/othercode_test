from datetime import datetime, timedelta
from functools import lru_cache

import bcrypt
import jwt

from src.core.settings import auth_settings


def encode_jwt(
    payload: dict,
    private_key: str = auth_settings.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = auth_settings.ALGORITHM,
    expire_timedelta: timedelta = None,
    expire_minutes: int = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


@lru_cache(maxsize=100)
def decode_jwt(
    token,
    public_key: str = auth_settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = auth_settings.ALGORITHM
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hash: str) -> bool:
    try:
        check_result = bcrypt.checkpw(password.encode(), hash.encode())
    except:
        return False
    return check_result
