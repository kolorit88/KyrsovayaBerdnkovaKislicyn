from sqlalchemy import *
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class MerchandiseVariation(Base):
    __tablename__ = 'merchandise_variations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    merchandise_id = Column(Integer, ForeignKey('merchandise.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    variation_text = Column(String(200), nullable=False)  # example: "полная порция (8 шт.)"
    weight_gram = Column(Integer, nullable=True)

    # Обратная связь
    merchandise = relationship("Merchandise", back_populates="variations")
    order_items = relationship("OrderItem", back_populates="variation")