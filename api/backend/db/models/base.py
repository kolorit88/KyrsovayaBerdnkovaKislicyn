from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass

# нельзя удалять импорты, нужно для правильной инициации
from backend.db.models.user import User
from backend.db.models.order import Order
from backend.db.models.order_item import OrderItem
from backend.db.models.merchandise import Merchandise
from backend.db.models.merchandise_variarions import MerchandiseVariation
from backend.db.models.merchandise_categories import MerchandiseCategory
from backend.db.models.refresh_token import RefreshToken
from backend.db.models.email_verification_token import EmailVerificationToken
from backend.db.models.password_reset_token import PasswordResetToken

