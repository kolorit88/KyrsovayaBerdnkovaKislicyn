from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

# --- Вариация ---
class MerchandiseVariationResponse(BaseModel):
    id: int
    quantity: int
    price: Decimal
    variation_text: str
    weight_gram: Optional[int] = None

    class Config:
        from_attributes = True  # раньше orm_mode

# --- Товар ---
class MerchandiseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image: str
    variations: List[MerchandiseVariationResponse] = []

    class Config:
        from_attributes = True

# --- Категория с товарами ---
class MerchandiseCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    merchandises: List[MerchandiseResponse] = []

    class Config:
        from_attributes = True

# --- Итоговый Response ---
class AllMerchandiseResponse(BaseModel):
    categories: List[MerchandiseCategoryResponse]