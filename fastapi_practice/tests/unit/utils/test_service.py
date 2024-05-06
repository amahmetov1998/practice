import pytest

from models import SpimexTradingResults
from src.services.trade import TradeService
from src.utils.repository import SqlAlchemyRepository
from tests.fakes.fixtures import TEST_REPO_GET_DATES, TEST_REPO_GET_TRADES_BY_DATE, TEST_REPO_GET_TRADES


class TestService:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        model = SpimexTradingResults

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_DATES)
    async def test_get_dates(self, kwargs, expected_result, expectation):

        sql_alchemy_repository = self._SqlAlchemyRepository
        service = TradeService(sql_alchemy_repository)

        with expectation:
            result = await service.get_dates(**kwargs)
            assert result == expected_result

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_TRADES)
    async def test_get_filtered_trades(self, kwargs, expected_result, expectation):

        sql_alchemy_repository = self._SqlAlchemyRepository
        service = TradeService(sql_alchemy_repository)

        with expectation:
            result = await service.get_filtered_trades(**kwargs)
            assert len(result) == expected_result

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_TRADES_BY_DATE)
    async def test_get_trading_results_by_date(self, kwargs, expected_result, expectation):

        sql_alchemy_repository = self._SqlAlchemyRepository
        service = TradeService(sql_alchemy_repository)

        with expectation:
            result = await service.get_trading_results_by_date(**kwargs)
            assert len(result) == expected_result
