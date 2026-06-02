from functools import lru_cache

from backend.application.services.order_service import OrderService
from backend.infrastructure.adapters.SqlAlchemy.order_alchemy_adapter import OrderAdapterSQLAlchemy
from backend.infrastructure.dependencies.auth import get_auth_adapter


@lru_cache()
def get_order_adapter() -> OrderAdapterSQLAlchemy:
    return OrderAdapterSQLAlchemy()


@lru_cache()
def get_order_service() -> OrderService:
    return OrderService(
        order_adapter=get_order_adapter(),
        auth_adapter=get_auth_adapter(),
    )