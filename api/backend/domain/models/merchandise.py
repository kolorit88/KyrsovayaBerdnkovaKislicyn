from typing import List
from attr import dataclass
from backend.domain.models.merchandise_variations import MerchandiseVariations


@dataclass
class Merchandise:
    id: int
    category_id : int
    name : str
    description : str
    image : str
    variations : List[MerchandiseVariations]

