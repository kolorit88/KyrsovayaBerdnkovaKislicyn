from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.db import async_session_maker
from backend.domain.ports.merchandise_port import MerchandisePort
from backend.db.models.base import *
from backend.infrastructure.dto.mappers.merchandise_mappers import MerchandiseCategoryMapper


class MerchandiseAdaptersSQLAlchemy(MerchandisePort):
    @classmethod
    async def get_all_merchandise_divided_into_categories(cls) -> List[MerchandiseCategory]:
        """Возвращает список всех товаров, разбитых по категориям."""
        async with async_session_maker() as session:
            stmt = (
                select(MerchandiseCategory)
                .options(
                    selectinload(MerchandiseCategory.merchandises)
                    .selectinload(Merchandise.variations)
                )
            )

            result = await session.execute(stmt)
            categories_orm = result.unique().scalars().all()

            return MerchandiseCategoryMapper.orm_list_to_domain(categories_orm)


if __name__ == '__main__':
    import asyncio

    # Вариант 1: для Windows с настройкой event loop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res = asyncio.run(MerchandiseAdaptersSQLAlchemy.get_all_merchandise_divided_into_categories())
    print(res)

