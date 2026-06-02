import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.config_load import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# --- Пароли ---

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# --- Access Token ---

def create_access_token(user_id: UUID, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

# --- Refresh Token ---

def generate_refresh_token() -> str:
    """Генерирует случайный opaque токен (не JWT)."""
    return secrets.token_urlsafe(64)

def hash_token(token: str) -> str:
    """SHA-256 хэш для хранения в БД."""
    return hashlib.sha256(token.encode()).hexdigest()

def refresh_token_expires_at() -> datetime:
    return datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

# --- Email tokens ---

def generate_email_token() -> str:
    return secrets.token_urlsafe(32)

def email_verification_expires_at() -> datetime:
    return datetime.utcnow() + timedelta(hours=24)

def password_reset_expires_at() -> datetime:
    return datetime.utcnow() + timedelta(hours=1)
