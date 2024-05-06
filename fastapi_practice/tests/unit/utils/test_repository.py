import pytest
from tests.fakes.fixtures import TEST_REPO_GET_DATES, TEST_REPO_GET_TRADES_BY_DATE, TEST_REPO_GET_TRADES
from src.models import SpimexTradingResults
from src.utils.repository import SqlAlchemyRepository


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        model = SpimexTradingResults

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_DATES)
    async def test_get_dates(self, kwargs, expected_result, expectation):
        sql_alchemy_repository = self._SqlAlchemyRepository()

        with expectation:
            result = await sql_alchemy_repository.get_dates(**kwargs)
            assert result == expected_result

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_TRADES)
    async def test_get_filtered_trades(self, kwargs, expected_result, expectation):
        sql_alchemy_repository = self._SqlAlchemyRepository()

        with expectation:
            result = await sql_alchemy_repository.get_filtered_trades(**kwargs)
            assert len(result) == expected_result

    @pytest.mark.parametrize("kwargs, expected_result, expectation", TEST_REPO_GET_TRADES_BY_DATE)
    async def test_get_trading_results_by_date(self, kwargs, expected_result, expectation):
        sql_alchemy_repository = self._SqlAlchemyRepository()

        with expectation:
            result = await sql_alchemy_repository.get_trading_results_by_date(**kwargs)
            assert len(result) == expected_result
