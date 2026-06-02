from typing import List

from backend.domain.models.merchandise_categories import MerchandiseCategory
from backend.domain.ports.merchandise_port import MerchandisePort
from backend.domain.services.merchandise_service_interface import MerchandiseServiceInterface


class MerchandiseService(MerchandiseServiceInterface):

    def __init__(self, merchandise_adapter: MerchandisePort):
        self._merchandise_adapter = merchandise_adapter

    async def get_all_merchandise_divided_into_categories(self) -> List[MerchandiseCategory]:
        """
        Возвращает список всех товаров через разбитых по категориям адаптер.
        """
        all_merchandise = await self._merchandise_adapter.get_all_merchandise_divided_into_categories()

        return all_merchandise