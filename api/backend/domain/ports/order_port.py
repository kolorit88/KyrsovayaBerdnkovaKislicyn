from abc import ABC, abstractmethod
from typing import List
from backend.domain.models.order import Order
from backend.domain.values import OrderStatus


class OrderPort(ABC):

    @abstractmethod
    async def create_order(
        self,
        user_id,
        user_name: str,
        user_email: str,
        user_phone_number: str,
        user_address: str,
        items: List[dict],
    ) -> Order:
        pass

    @abstractmethod
    async def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    async def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: int, status: OrderStatus) -> Order:
        pass