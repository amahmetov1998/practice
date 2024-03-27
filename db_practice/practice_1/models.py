import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
)]

updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]


class Genre(Base):

    __tablename__ = 'genre'

    id: Mapped[intpk]
    genre_name: Mapped[str]

    genre_books: Mapped[list['Book']] = relationship(back_populates='genre')


class Author(Base):

    __tablename__ = 'author'

    id: Mapped[intpk]
    author_name: Mapped[str]

    author_books: Mapped[list['Book']] = relationship(back_populates='author')


class Book(Base):

    __tablename__ = 'book'

    id: Mapped[intpk]
    book_title: Mapped[str]
    price: Mapped[int]
    amount_in_stock: Mapped[int]

    genre_id: Mapped[int] = mapped_column(ForeignKey('genre.id', ondelete='CASCADE'))
    genre: Mapped['Genre'] = relationship(
        back_populates='genre_books',
    )

    author_id: Mapped[int] = mapped_column(ForeignKey('author.id', ondelete='CASCADE'))
    author: Mapped['Author'] = relationship(
        back_populates='author_books',
    )


class City(Base):
    __tablename__ = 'city'

    id: Mapped[intpk]
    city_name: Mapped[str]
    delivery_time: Mapped[int]

    city_clients: Mapped[list['Client']] = relationship(back_populates='city')


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[intpk]
    client_name: Mapped[str]
    email = Mapped[str]

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id', ondelete='CASCADE'))
    city: Mapped['City'] = relationship(
        back_populates='city_clients',
    )

    client_order: Mapped[list['Buy']] = relationship(
        back_populates='client',
    )


class Buy(Base):
    __tablename__ = 'buy'

    id: Mapped[intpk]
    order_description: Mapped[str]

    client_id: Mapped[int] = mapped_column(ForeignKey('client.id', ondelete='CASCADE'))
    client: Mapped['Client'] = relationship(
        back_populates='client_order',
    )

    orders: Mapped[list['BuyBook']] = relationship(
        back_populates='order',
    )

    steps: Mapped[list['BuyStep']] = relationship(
        back_populates='buy',
    )


class BuyBook(Base):
    __tablename__ = 'buy_book'

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('buy.id', ondelete='CASCADE'))
    order: Mapped['Buy'] = relationship(
        back_populates='orders',
    )


class Step(Base):
    __tablename__ = 'step'

    id: Mapped[intpk]
    step_name: Mapped[str]
    order_steps: Mapped[list['BuyStep']] = relationship(
        back_populates='step',
    )


class BuyStep(Base):
    __tablename__ = 'buy_step'

    id: Mapped[intpk]

    step_id: Mapped[int] = mapped_column(ForeignKey('step.id', ondelete='CASCADE'))
    step: Mapped['Step'] = relationship(
        back_populates='order_steps',
    )

    order_id: Mapped[int] = mapped_column(ForeignKey('buy.id', ondelete='CASCADE'))
    buy: Mapped['Buy'] = relationship(
        back_populates='steps',
    )

    step_start_date: Mapped[created_at]
    step_end_date: Mapped[updated_at]
