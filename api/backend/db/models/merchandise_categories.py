from sqlalchemy import *
from sqlalchemy.orm import relationship
from backend.db.models.base import Base

class MerchandiseCategory(Base):
    __tablename__ = 'merchandise_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)  # "роллы"
    slug = Column(String(100), nullable=False, unique=True)  # "rolls" (для URL/API)
    description = Column(String(250), nullable=True) # это вроде не нужно, но пока оставлю

    # Связь с товарами
    merchandises = relationship("Merchandise", back_populates="category")