from datetime import datetime

from attr import dataclass
from uuid import UUID

from backend.domain.values import Role


@dataclass
class User:
    id: UUID
    name: str
    email: str
    phone_number: str
    address: str
    hashed_password: str

    created_at: datetime
    updated_at : datetime

    is_active: bool = True
    role: Role = Role.USER