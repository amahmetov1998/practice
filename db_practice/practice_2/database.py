from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL


engine = create_engine(url=DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)
