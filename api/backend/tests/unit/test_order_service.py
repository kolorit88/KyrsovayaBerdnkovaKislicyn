"""
Unit-тесты для OrderService.

Все зависимости (OrderPort, AuthPort) мокаются — БД не нужна.
Запуск: pytest tests/unit/test_order_service.py -v
"""

from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.application.services.order_service import OrderService
from backend.domain.models.order import Order
from backend.domain.models.order_item import OrderItem
from backend.domain.models.user import User
from backend.domain.values import OrderStatus, Role


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def make_user(**kwargs) -> User:
    defaults = dict(
        id=uuid4(),
        name="Тест Тестов",
        email="test@example.com",
        phone_number="+79000000000",
        address="ул. Тестовая, 1",
        hashed_password="hash",
        is_active=True,
        role=Role.USER,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    defaults.update(kwargs)
    return User(**defaults)


def make_order(user_id=None, status=OrderStatus.PENDING) -> Order:
    uid = user_id or uuid4()
    return Order(
        id=1,
        user_id=uid,
        user_name="Тест Тестов",
        user_email="test@example.com",
        user_phone_number="+79000000000",
        user_address="ул. Тестовая, 1",
        created_at=datetime.utcnow(),
        status=status,
        items=[
            OrderItem(
                id=1,
                order_id=1,
                variation_id=10,
                quantity=2,
                price_at_time=Decimal("450.00"),
            )
        ],
    )


def make_services(user=None, order=None):
    """Создаёт пару замоканных адаптеров и OrderService."""
    order_adapter = AsyncMock()
    auth_adapter = AsyncMock()

    auth_adapter.get_user_by_id.return_value = user or make_user()
    order_adapter.create_order.return_value = order or make_order()
    order_adapter.get_all_orders.return_value = [make_order(), make_order(status=OrderStatus.COMPLETED)]
    order_adapter.get_orders_by_status.return_value = [make_order()]
    order_adapter.get_order_by_id.return_value = make_order()
    order_adapter.update_order_status.return_value = make_order(status=OrderStatus.COMPLETED)

    service = OrderService(order_adapter=order_adapter, auth_adapter=auth_adapter)
    return service, order_adapter, auth_adapter


# ─────────────────────────────────────────────
# create_order()
# ─────────────────────────────────────────────

class TestCreateOrder:
    @pytest.mark.asyncio
    async def test_create_order_passes_user_fields_to_adapter(self):
        """create_order заполняет поля пользователя из AuthPort, а не от клиента."""
        user = make_user(name="Иван", email="ivan@mail.ru", address="Питер")
        service, order_adapter, _ = make_services(user=user)

        items = [{"variation_id": 5, "quantity": 3}]
        await service.create_order(user_id=user.id, items=items)

        order_adapter.create_order.assert_awaited_once()
        call_kwargs = order_adapter.create_order.call_args.kwargs
        assert call_kwargs["user_name"] == "Иван"
        assert call_kwargs["user_email"] == "ivan@mail.ru"
        assert call_kwargs["user_address"] == "Питер"
        assert call_kwargs["items"] == items

    @pytest.mark.asyncio
    async def test_create_order_user_not_found_raises_404(self):
        """Если пользователь не найден — HTTP 404."""
        from fastapi import HTTPException

        service, _, auth_adapter = make_services()
        auth_adapter.get_user_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await service.create_order(user_id=uuid4(), items=[{"variation_id": 1, "quantity": 1}])

        assert exc_info.value.status_code == 404


# ─────────────────────────────────────────────
# get_pending_orders() / get_completed_orders()
# ─────────────────────────────────────────────

class TestGetOrdersByStatus:
    @pytest.mark.asyncio
    async def test_get_pending_orders_calls_adapter_with_pending_status(self):
        service, order_adapter, _ = make_services()

        await service.get_pending_orders()

        order_adapter.get_orders_by_status.assert_awaited_once_with(OrderStatus.PENDING)

    @pytest.mark.asyncio
    async def test_get_completed_orders_calls_adapter_with_completed_status(self):
        service, order_adapter, _ = make_services()

        await service.get_completed_orders()

        order_adapter.get_orders_by_status.assert_awaited_once_with(OrderStatus.COMPLETED)


# ─────────────────────────────────────────────
# get_order_by_id()
# ─────────────────────────────────────────────

class TestGetOrderById:
    @pytest.mark.asyncio
    async def test_returns_order_when_found(self):
        service, order_adapter, _ = make_services()
        order_adapter.get_order_by_id.return_value = make_order()

        result = await service.get_order_by_id(1)

        assert result.id == 1

    @pytest.mark.asyncio
    async def test_raises_404_when_not_found(self):
        from fastapi import HTTPException

        service, order_adapter, _ = make_services()
        order_adapter.get_order_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await service.get_order_by_id(999)

        assert exc_info.value.status_code == 404


# ─────────────────────────────────────────────
# update_order_status()
# ─────────────────────────────────────────────

class TestUpdateOrderStatus:
    @pytest.mark.asyncio
    async def test_update_status_delegates_to_adapter(self):
        service, order_adapter, _ = make_services()
        completed_order = make_order(status=OrderStatus.COMPLETED)
        order_adapter.update_order_status.return_value = completed_order

        result = await service.update_order_status(1, OrderStatus.COMPLETED)

        order_adapter.update_order_status.assert_awaited_once_with(1, OrderStatus.COMPLETED)
        assert result.status == OrderStatus.COMPLETED