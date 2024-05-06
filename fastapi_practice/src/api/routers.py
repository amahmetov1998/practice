from datetime import datetime
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.repositories.trade import TradeRepository
from src.timer import expired_time
from src.services.trade import TradeService
router = APIRouter(prefix="/api", tags=['Trade'])


@router.get("/last_dates")
@cache(expire=expired_time(hour=11, minute=23))
async def get_last_trading_dates(date_num: int = 10):

    result = await TradeService(TradeRepository).get_dates(date_num)

    return result


@router.get("/trades_by_date")
@cache(expire=expired_time(hour=11, minute=23))
async def get_dynamics(
        start_date: datetime,
        end_date: datetime,
        oil_id: str = "A592",
        delivery_type_id: str = "A",
        delivery_basis_id: str = "ZHL"):

    result = await TradeService(TradeRepository).get_filtered_trades_between_dates(
        start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
    )

    return result


@router.get("/last_trades")
@cache(expire=expired_time(hour=11, minute=23))
async def get_trading_results(oil_id: str = "A592", delivery_type_id: str = "A", delivery_basis_id: str = "ZHL"):

    date = await TradeService(TradeRepository).get_last_date()
    result = await TradeService(TradeRepository).get_trading_results_by_date(
        date, oil_id, delivery_type_id, delivery_basis_id
    )

    return result
