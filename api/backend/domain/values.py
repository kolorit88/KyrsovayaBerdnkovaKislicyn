from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

# не используется, фактически заполняется в миграциях alembic
class MerchandiseCategories(str, Enum):
    BUSINESS_LUNCH = 'business-lunch'
    MINI_ROLLS = 'mini-rolls'
    ROLLS = 'rolls'
    FRIED_ROLLS = 'fried-rolls'
    BAKED_ROLLS = 'baked-rolls'
    PIZZA = 'pizza'
    WOK = 'wok-noodles'
    ADDITIONAL_MERCHANDISE = 'additional'
    DRINKS = 'drinks'

    @property
    def display_name(self):
        """Возвращает человекочитаемое название"""
        names = {
            'business-lunch': 'бизнес-ланч',
            'mini-rolls': 'роллы мини',
            'rolls': 'роллы',
            'fried-rolls': 'жареные роллы',
            'baked-rolls': 'запеченные роллы',
            'pizza': 'пицца',
            'wok-noodles': 'лапша wok',
            'additional': 'сопутствующие товары',
            'drinks': 'напитки',
        }
        return names[self.value]