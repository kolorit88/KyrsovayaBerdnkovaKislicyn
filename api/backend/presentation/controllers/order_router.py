from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.application.services.order_service import OrderService
from backend.domain.values import Role
from backend.infrastructure.dependencies.current_user import get_current_user_id
from backend.infrastructure.dependencies.order import get_order_service
from backend.infrastructure.dto.requests.order_dto import CreateOrderRequest, UpdateOrderStatusRequest
from backend.infrastructure.dto.responses.order_dto import OrderResponse, OrderListResponse
from backend.infrastructure.utils.security import decode_access_token

router = APIRouter(prefix="/orders", tags=["orders"])


def _require_high_rights(request: Request) -> None:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")
    payload = decode_access_token(token)
    if not payload or payload.get("role") not in (Role.ADMIN.value, Role.MODERATOR.value):
        raise HTTPException(status_code=403, detail="Нет доступа")


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    body: CreateOrderRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: OrderService = Depends(get_order_service),
):
    """Создать заказ. Цены берутся из БД, не от клиента."""
    items = [{"variation_id": i.variation_id, "quantity": i.quantity} for i in body.items]
    return await service.create_order(user_id=user_id, items=items)


@router.get("", response_model=OrderListResponse)
async def get_all_orders(
    request: Request,
    service: OrderService = Depends(get_order_service),
):
    """Все заказы — только для admin/moderator."""
    _require_high_rights(request)
    orders = await service.get_all_orders()
    return OrderListResponse(orders=orders)


@router.get("/pending", response_model=OrderListResponse)
async def get_pending_orders(
    request: Request,
    service: OrderService = Depends(get_order_service),
):
    """Заказы со статусом PENDING — только для admin/moderator."""
    _require_high_rights(request)
    orders = await service.get_pending_orders()
    return OrderListResponse(orders=orders)


@router.get("/completed", response_model=OrderListResponse)
async def get_completed_orders(
    request: Request,
    service: OrderService = Depends(get_order_service),
):
    """Заказы со статусом COMPLETED — только для admin/moderator."""
    _require_high_rights(request)
    orders = await service.get_completed_orders()
    return OrderListResponse(orders=orders)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    request: Request,
    service: OrderService = Depends(get_order_service),
):
    """Детали заказа — только для admin/moderator."""
    _require_high_rights(request)
    return await service.get_order_by_id(order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    body: UpdateOrderStatusRequest,
    request: Request,
    service: OrderService = Depends(get_order_service),
):
    _require_high_rights(request)
    return await service.update_order_status(order_id, body.status)