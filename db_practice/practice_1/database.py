from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(url=DATABASE_URL)

session = sessionmaker(bind=engine)
