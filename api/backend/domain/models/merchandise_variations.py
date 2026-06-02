from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MerchandiseVariations:
    id : int
    merchandise_id : int
    quantity : int
    price: Decimal
    variation_text: str # example: "полная порция (8 шт.)"
    weight_gram : int