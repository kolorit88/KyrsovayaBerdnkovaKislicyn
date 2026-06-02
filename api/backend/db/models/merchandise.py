from sqlalchemy import *
from sqlalchemy.orm import relationship

from backend.db.models.base import Base

class Merchandise(Base):
    __tablename__ = 'merchandise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('merchandise_categories.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=True)
    image = Column(String, nullable=False)

    # Связь с вариациями
    category = relationship("MerchandiseCategory", back_populates="merchandises")
    variations = relationship("MerchandiseVariation", back_populates="merchandise",
                              cascade="all, delete-orphan")