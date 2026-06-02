from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID
from backend.domain.models.order_item import OrderItem
from backend.domain.values import OrderStatus


@dataclass
class Order:
    id: int
    user_id: UUID
    user_name: str
    user_email: str
    user_phone_number: str
    user_address: str
    created_at: datetime
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING.value