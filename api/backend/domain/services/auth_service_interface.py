from abc import ABC, abstractmethod
from uuid import UUID


class AuthServiceInterface(ABC):

    @abstractmethod
    async def register(self, name: str, email: str, phone_number: str, address: str, password: str) -> dict:
        pass

    @abstractmethod
    async def verify_email(self, token: str) -> dict:
        pass

    @abstractmethod
    async def login(self, login: str, password: str) -> dict:
        """login — email or phone_number"""
        pass

    @abstractmethod
    async def logout(self, refresh_token: str) -> None:
        pass

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> dict:
        pass

    @abstractmethod
    async def get_me(self, user_id: UUID) -> dict:
        pass

    @abstractmethod
    async def update_me(self, user_id: UUID, **fields) -> dict:
        pass

    @abstractmethod
    async def change_password(self, user_id: UUID, old_password: str, new_password: str) -> None:
        pass

    @abstractmethod
    async def request_password_reset(self, email: str) -> None:
        pass

    @abstractmethod
    async def reset_password(self, token: str, new_password: str) -> None:
        pass
