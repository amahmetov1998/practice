from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL_SYNC, DATABASE_URL_ASYNC


sync_engine = create_engine(url=DATABASE_URL_SYNC)
sync_session = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(url=DATABASE_URL_ASYNC)
async_session = async_sessionmaker(bind=async_engine)
