from typing import Type

from src.utils.repository import AbstractRepository


class TradeService:
    def __init__(self, repo: Type[AbstractRepository]):
        self.repo = repo()

    async def get_dates(self, date_num):
        result = await self.repo.get_dates(date_num)
        return result

    async def get_filtered_trades(self, start_date, end_date, oil_id, delivery_type_id, delivery_basis_id):
        result = await self.repo.get_filtered_trades(
            start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
        )
        return result

    async def get_last_date(self):
        result = await self.repo.get_last_date()
        return result

    async def get_trading_results_by_date(self, date, oil_id, delivery_type_id, delivery_basis_id):
        result = await self.repo.get_trading_results_by_date(date, oil_id, delivery_type_id, delivery_basis_id)
        return result
