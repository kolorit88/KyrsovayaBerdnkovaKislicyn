from typing import List
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.db import async_session_maker
from backend.db.models.base import Order as OrderORM, OrderItem as OrderItemORM
from backend.db.models.merchandise_variarions import MerchandiseVariation
from backend.domain.models.order import Order as OrderDomain
from backend.domain.models.order_item import OrderItem as OrderItemDomain
from backend.domain.ports.order_port import OrderPort
from backend.domain.values import OrderStatus
from fastapi import HTTPException
from sqlalchemy import update as sa_update


class OrderAdapterSQLAlchemy(OrderPort):

    async def create_order(
        self,
        user_id: UUID,
        user_name: str,
        user_email: str,
        user_phone_number: str,
        user_address: str,
        items: List[dict],
    ) -> OrderDomain:
        async with async_session_maker() as session:
            variation_ids = [item["variation_id"] for item in items]
            result = await session.execute(
                select(MerchandiseVariation).where(
                    MerchandiseVariation.id.in_(variation_ids)
                )
            )
            variations = {v.id: v for v in result.scalars().all()}

            for item in items:
                if item["variation_id"] not in variations:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Вариация {item['variation_id']} не найдена"
                    )

            order_orm = OrderORM(
                user_id=user_id,
                user_name=user_name,
                user_email=user_email,
                user_phone_number=user_phone_number,
                user_address=user_address,
            )
            session.add(order_orm)
            await session.flush()

            order_items = []
            for item in items:
                variation = variations[item["variation_id"]]
                item_orm = OrderItemORM(
                    order_id=order_orm.id,
                    variation_id=item["variation_id"],
                    quantity=item["quantity"],
                    price_at_time=variation.price,
                )
                session.add(item_orm)
                order_items.append(item_orm)

            await session.commit()
            await session.refresh(order_orm)

            return self._orm_to_domain(order_orm, order_items)

    async def get_all_orders(self) -> List[OrderDomain]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(OrderORM)
                .options(selectinload(OrderORM.items))
                .order_by(OrderORM.created_at.desc())
            )
            orders = result.unique().scalars().all()
            return [self._orm_to_domain(o, o.items) for o in orders]

    async def get_orders_by_status(self, status: OrderStatus) -> List[OrderDomain]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(OrderORM)
                .options(selectinload(OrderORM.items))
                .where(OrderORM.status == status)
                .order_by(OrderORM.created_at.desc())
            )
            orders = result.unique().scalars().all()
            return [self._orm_to_domain(o, o.items) for o in orders]

    async def get_order_by_id(self, order_id: int) -> OrderDomain | None:
        async with async_session_maker() as session:
            result = await session.execute(
                select(OrderORM)
                .options(selectinload(OrderORM.items))
                .where(OrderORM.id == order_id)
            )
            order = result.scalar_one_or_none()
            if not order:
                return None
            return self._orm_to_domain(order, order.items)

    async def update_order_status(self, order_id: int, status: OrderStatus) -> OrderDomain:
        async with async_session_maker() as session:
            await session.execute(
                sa_update(OrderORM)
                .where(OrderORM.id == order_id)
                .values(status=status)
            )
            await session.commit()

        order = await self.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        return order

    @staticmethod
    def _orm_to_domain(order_orm: OrderORM, items) -> OrderDomain:
        return OrderDomain(
            id=order_orm.id,
            user_id=order_orm.user_id,
            user_name=order_orm.user_name,
            user_email=order_orm.user_email,
            user_phone_number=order_orm.user_phone_number,
            user_address=order_orm.user_address,
            created_at=order_orm.created_at,
            status=order_orm.status,
            items=[
                OrderItemDomain(
                    id=i.id,
                    order_id=i.order_id,
                    variation_id=i.variation_id,
                    quantity=i.quantity,
                    price_at_time=Decimal(str(i.price_at_time)),
                )
                for i in items
            ],
        )