from abc import ABC, abstractmethod
from typing import List
from backend.domain.models.merchandise_categories import MerchandiseCategory


class MerchandisePort(ABC):

    @abstractmethod
    async def get_all_merchandise_divided_into_categories(self) -> List[MerchandiseCategory]:
        pass


