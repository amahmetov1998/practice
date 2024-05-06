from abc import ABC, abstractmethod

from sqlalchemy import select, distinct, desc

from src.database.db import async_session_maker


class AbstractRepository(ABC):

    @abstractmethod
    async def get_dates(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_filtered_trades(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_last_date(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_trading_results_by_date(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    async def get_dates(self, date_num):
        async with async_session_maker() as session:
            query = select(distinct(self.model.date)).order_by(desc(self.model.date)).limit(date_num)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_filtered_trades(self, start_date, end_date, oil_id, delivery_type_id, delivery_basis_id):
        async with async_session_maker() as session:
            query = select(self.model).where(
                self.model.date.between(start_date, end_date)
            ).filter(
                self.model.oil_id == oil_id,
                self.model.delivery_type_id == delivery_type_id,
                self.model.delivery_basis_id == delivery_basis_id
            )
            result = await session.execute(query)

            return result.scalars().all()

    async def get_last_date(self):
        async with async_session_maker() as session:
            query = select(self.model.date).order_by(desc(self.model.date)).limit(1)
            result = await session.execute(query)

            return result.scalars().first()

    async def get_trading_results_by_date(self, date, oil_id, delivery_type_id, delivery_basis_id):

        async with async_session_maker() as session:
            query = select(self.model).where(self.model.date == date).filter(
                self.model.oil_id == oil_id,
                self.model.delivery_type_id == delivery_type_id,
                self.model.delivery_basis_id == delivery_basis_id
            )

            result = await session.execute(query)
            return result.scalars().all()
