from datetime import datetime
from uuid import uuid4

from sqlalchemy import *
from backend.db.models.base import Base
from backend.domain.values import Role


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    address = Column(String(500), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(
        Enum(Role, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=Role.USER
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)