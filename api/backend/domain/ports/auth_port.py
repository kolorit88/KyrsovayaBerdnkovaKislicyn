from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from backend.domain.models.user import User


class AuthPort(ABC):

    # --- User ---

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(
        self,
        name: str,
        email: str,
        phone_number: str,
        address: str,
        hashed_password: str,
    ) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: UUID, **fields) -> User:
        pass

    # --- Email verification ---

    @abstractmethod
    async def create_email_verification_token(self, user_id: UUID, token: str, expires_at: datetime) -> None:
        pass

    @abstractmethod
    async def get_email_verification_token(self, token: str) -> Optional[dict]:
        """Returns dict with keys: user_id, expires_at, used"""
        pass

    @abstractmethod
    async def mark_email_token_used(self, token: str) -> None:
        pass

    # --- Password reset ---

    @abstractmethod
    async def create_password_reset_token(self, user_id: UUID, token: str, expires_at: datetime) -> None:
        pass

    @abstractmethod
    async def get_password_reset_token(self, token: str) -> Optional[dict]:
        """Returns dict with keys: user_id, expires_at, used"""
        pass

    @abstractmethod
    async def mark_password_reset_token_used(self, token: str) -> None:
        pass

    # --- Refresh tokens ---

    @abstractmethod
    async def save_refresh_token(self, user_id: UUID, token_hash: str, expires_at: datetime) -> None:
        pass

    @abstractmethod
    async def get_refresh_token(self, token_hash: str) -> Optional[dict]:
        """Returns dict with keys: user_id, expires_at, revoked"""
        pass

    @abstractmethod
    async def revoke_refresh_token(self, token_hash: str) -> None:
        pass

    @abstractmethod
    async def revoke_all_user_refresh_tokens(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def delete_email_verification_tokens(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def delete_expired_refresh_tokens(self) -> int:
        pass
