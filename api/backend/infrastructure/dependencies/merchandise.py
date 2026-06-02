from functools import lru_cache

from backend.domain.ports.merchandise_port import MerchandisePort
from backend.application.services.merchandise_service import MerchandiseService
from backend.infrastructure.adapters.SqlAlchemy.merchandise_alchemy_adapter import MerchandiseAdaptersSQLAlchemy


@lru_cache()
def get_merchandise_adapter() -> MerchandisePort:
    return MerchandiseAdaptersSQLAlchemy()

@lru_cache()
def get_merchandise_service() -> MerchandiseService:
    adapter = get_merchandise_adapter()
    return MerchandiseService(adapter)