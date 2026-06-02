from pydantic import BaseModel, field_validator
from typing import List
from decimal import Decimal
from backend.domain.values import OrderStatus



class OrderItemRequest(BaseModel):
    variation_id: int
    quantity: int


    @classmethod
    @field_validator("quantity")
    def quantity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Количество должно быть не менее 1")
        return v


class CreateOrderRequest(BaseModel):
    items: List[OrderItemRequest]


    @classmethod
    @field_validator("items")
    def items_not_empty(cls, v):
        if not v:
            raise ValueError("Заказ должен содержать хотя бы один товар")
        return v

class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus