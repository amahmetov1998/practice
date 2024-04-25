from src.models import SpimexTradingResults
from src.utils.repository import SqlAlchemyRepository


class TradeRepository(SqlAlchemyRepository):
    model = SpimexTradingResults
