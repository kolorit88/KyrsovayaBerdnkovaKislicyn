from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItem:
    id : int
    order_id : int
    variation_id : int
    quantity : int
    price_at_time : Decimal

