from dataclasses import dataclass


@dataclass
class MerchandiseCategory:
    id : int
    name : str  # "роллы"
    slug : str  # "rolls" (для URL/API)
    description : str  # это вроде не нужно, но пока оставлю
    merchandises: list
