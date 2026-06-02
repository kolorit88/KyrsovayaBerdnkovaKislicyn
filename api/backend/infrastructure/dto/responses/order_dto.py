from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime


class OrderItemResponse(BaseModel):
    id: int
    variation_id: int
    quantity: int
    price_at_time: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_name: str
    user_email: str
    user_phone_number: str
    user_address: str
    created_at: datetime
    items: List[OrderItemResponse]
    status: str

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]