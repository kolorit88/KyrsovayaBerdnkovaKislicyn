from datetime import datetime
from uuid import uuid4

from sqlalchemy import *
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class EmailVerificationToken(Base):
    __tablename__ = 'email_verification_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    used = Column(Boolean, default=False, nullable=False)

    user = relationship("User", backref="email_verification_tokens")

