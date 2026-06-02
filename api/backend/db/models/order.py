from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship

from backend.db.models.base import Base
from backend.domain.values import OrderStatus


#специально не ссылаемся на поля пользователя для истории заказов
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey('user.id'))
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=False, index=True)
    user_phone_number = Column(String(20), nullable=False, unique=False)
    user_address = Column(String(500), nullable=False)
    status = Column(
        Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=OrderStatus.PENDING
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")