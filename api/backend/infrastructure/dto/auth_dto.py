from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
import re


# ------------------------------------------------------------------ #
#  Requests                                                            #
# ------------------------------------------------------------------ #

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str
    password: str

    @classmethod
    @field_validator("password")
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v

    @classmethod
    @field_validator("phone_number")
    def phone_format(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?\d{10,15}$", cleaned):
            raise ValueError("Некорректный номер телефона")
        return cleaned


class LoginRequest(BaseModel):
    login: str   # email или номер телефона
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class VerifyEmailRequest(BaseModel):
    token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @classmethod
    @field_validator("new_password")
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v


class RequestPasswordResetRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @classmethod
    @field_validator("new_password")
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v


class UpdateMeRequest(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    # email намеренно не меняем здесь — смена email требует повторной верификации


# ------------------------------------------------------------------ #
#  Responses                                                           #
# ------------------------------------------------------------------ #

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone_number: str
    address: str
    role: str
    is_active: bool
    created_at: datetime
