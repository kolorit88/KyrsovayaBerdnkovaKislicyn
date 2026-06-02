from typing import List
from uuid import UUID

from fastapi import HTTPException

from backend.domain.models.order import Order
from backend.domain.ports.order_port import OrderPort
from backend.domain.ports.auth_port import AuthPort
from backend.domain.values import OrderStatus


class OrderService:

    def __init__(self, order_adapter: OrderPort, auth_adapter: AuthPort):
        self._order_adapter = order_adapter
        self._auth_adapter = auth_adapter

    async def create_order(self, user_id: UUID, items: List[dict]) -> Order:
        user = await self._auth_adapter.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        return await self._order_adapter.create_order(
            user_id=user.id,
            user_name=user.name,
            user_email=user.email,
            user_phone_number=user.phone_number,
            user_address=user.address,
            items=items,
        )

    async def get_all_orders(self) -> List[Order]:
        return await self._order_adapter.get_all_orders()

    async def get_pending_orders(self) -> List[Order]:
        return await self._order_adapter.get_orders_by_status(OrderStatus.PENDING)

    async def get_completed_orders(self) -> List[Order]:
        return await self._order_adapter.get_orders_by_status(OrderStatus.COMPLETED)

    async def get_order_by_id(self, order_id: int) -> Order:
        order = await self._order_adapter.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        return order

    async def update_order_status(self, order_id: int, status: OrderStatus) -> Order:
        return await self._order_adapter.update_order_status(order_id, status)