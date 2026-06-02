from functools import lru_cache

from backend.domain.ports.auth_port import AuthPort
from backend.application.services.auth_service import AuthService
from backend.infrastructure.adapters.SqlAlchemy.auth_alchemy_adapter import AuthAdapterSQLAlchemy


@lru_cache()
def get_auth_adapter() -> AuthPort:
    return AuthAdapterSQLAlchemy()


@lru_cache()
def get_auth_service() -> AuthService:
    adapter = get_auth_adapter()
    return AuthService(adapter)
