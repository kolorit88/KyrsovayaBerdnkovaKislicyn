from sqlalchemy import *
from sqlalchemy.orm import relationship
from backend.db.models.base import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    variation_id = Column(Integer, ForeignKey('merchandise_variations.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_time = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    variation = relationship("MerchandiseVariation")