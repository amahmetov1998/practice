import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass


created_on = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
)]

updated_on = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int | None]
    total: Mapped[int | None]
    count: Mapped[int | None]
    date: Mapped[datetime.date]
    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]
