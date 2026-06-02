from typing import List
from decimal import Decimal

from backend.db.models.merchandise import Merchandise as MerchandiseORM
from backend.db.models.merchandise_variarions import MerchandiseVariation as MerchandiseVariationORM
from backend.db.models.merchandise_categories import MerchandiseCategory as MerchandiseCategoryORM
from backend.domain.models.merchandise import Merchandise as MerchandiseDomain
from backend.domain.models.merchandise_variations import MerchandiseVariations as MerchandiseVariationsDomain
from backend.domain.models.merchandise_categories import MerchandiseCategory as MerchandiseCategoryDomain


class MerchandiseVariationMapper:
    """Маппер для вариаций товара (самый нижний уровень)"""

    @staticmethod
    def orm_to_domain(orm_model: MerchandiseVariationORM) -> MerchandiseVariationsDomain:
        return MerchandiseVariationsDomain(
            id=orm_model.id,
            merchandise_id=orm_model.merchandise_id,
            quantity=orm_model.quantity,
            price=Decimal(str(orm_model.price)) if orm_model.price else Decimal('0.00'),
            variation_text=orm_model.variation_text,
            weight_gram=orm_model.weight_gram or 0
        )

    @staticmethod
    def domain_to_orm(domain_model: MerchandiseVariationsDomain) -> MerchandiseVariationORM:
        return MerchandiseVariationORM(
            id=domain_model.id,
            merchandise_id=domain_model.merchandise_id,
            quantity=domain_model.quantity,
            price=domain_model.price,
            variation_text=domain_model.variation_text,
            weight_gram=domain_model.weight_gram
        )

    @staticmethod
    def orm_list_to_domain(orm_list: List[MerchandiseVariationORM]) -> List[MerchandiseVariationsDomain]:
        return [MerchandiseVariationMapper.orm_to_domain(item) for item in orm_list]


class MerchandiseMapper:
    """Маппер для товаров (средний уровень, включает вариации)"""

    @staticmethod
    def orm_to_domain(orm_model: MerchandiseORM) -> MerchandiseDomain:
        return MerchandiseDomain(
            id=orm_model.id,
            category_id=orm_model.category_id,
            name=orm_model.name,
            description=orm_model.description or "",
            image=orm_model.image,
            variations=MerchandiseVariationMapper.orm_list_to_domain(orm_model.variations)
            if orm_model.variations else []
        )

    @staticmethod
    def domain_to_orm(domain_model: MerchandiseDomain) -> MerchandiseORM:
        return MerchandiseORM(
            id=domain_model.id,
            category_id=domain_model.category_id,
            name=domain_model.name,
            description=domain_model.description,
            image=domain_model.image
        )

    @staticmethod
    def orm_list_to_domain(orm_list: List[MerchandiseORM]) -> List[MerchandiseDomain]:
        return [MerchandiseMapper.orm_to_domain(item) for item in orm_list]


class MerchandiseCategoryMapper:
    """Маппер для категорий (верхний уровень, включает товары с вариациями)"""

    @staticmethod
    def orm_to_domain(orm_model: MerchandiseCategoryORM) -> MerchandiseCategoryDomain:
        return MerchandiseCategoryDomain(
            id=orm_model.id,
            name=orm_model.name,
            slug=orm_model.slug,
            description=orm_model.description or "",
            merchandises=MerchandiseMapper.orm_list_to_domain(orm_model.merchandises)
            if orm_model.merchandises else []
        )

    @staticmethod
    def domain_to_orm(domain_model: MerchandiseCategoryDomain) -> MerchandiseCategoryORM:
        return MerchandiseCategoryORM(
            id=domain_model.id,
            name=domain_model.name,
            slug=domain_model.slug,
            description=domain_model.description
        )

    @staticmethod
    def orm_list_to_domain(orm_list: List[MerchandiseCategoryORM]) -> List[MerchandiseCategoryDomain]:
        return [MerchandiseCategoryMapper.orm_to_domain(item) for item in orm_list]