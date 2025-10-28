from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Dict[str, Any], expires_minutes: int | None = None) -> str:
    expire_minutes = expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload: Dict[str, Any]
    if isinstance(subject, dict):
        payload = subject.copy()
    else:
        payload = {"sub": subject}
    payload.update({"exp": expire_at})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # raises on invalid/expired


