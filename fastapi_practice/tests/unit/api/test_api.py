from httpx import AsyncClient
from src.api.routers import get_last_trading_dates

async def test_get_last_trading_dates(ac: AsyncClient):
    response = await ac.get('api/last_dates', params={"date_num": 15})

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 15


async def test_get_dynamics(ac: AsyncClient):
    response = await ac.get('api/trades_by_date', params={"start_date": "2024-04-15",
                                                          "end_date": "2024-04-22"})

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 6


async def test_get_trading_results(ac: AsyncClient):
    response = await ac.get('api/last_trades')

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 1
