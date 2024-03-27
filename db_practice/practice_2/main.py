from database import engine, session
from models import Base
from html_parser import parse_html
from excel_parser import parse_excel
from models import SpimexTradingResults


class ORM:

    @staticmethod
    def create_table():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def parse_html():
        return parse_html()

    @staticmethod
    def parse_excel():
        return parse_excel()

    @classmethod
    def insert_data(cls):
        for arg in cls.parse_excel():
            with session() as s:
                line = SpimexTradingResults(**arg)
                s.add(line)
                s.commit()


if __name__ == '__main__':
    ORM.create_table()
    ORM.parse_html()
    ORM.parse_excel()
    ORM.insert_data()
