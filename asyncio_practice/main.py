import asyncio

from models import Base, SpimexTradingResults
from database import sync_engine, sync_session, async_session
from downloader import sync_download_file, main
from excel_parser import parse_excel
import time


class SYNC:
    @staticmethod
    def create_table():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def download():
        return sync_download_file()

    @staticmethod
    def insert_data():
        for arg in parse_excel():
            with sync_session() as s:
                line = SpimexTradingResults(**arg)
                s.add(line)
                s.commit()


class ASYNC:

    @staticmethod
    def create_table():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def download():
        return main()

    @staticmethod
    async def insert_data():
        async with async_session() as s:
            lines = []
            for arg in parse_excel():
                line = SpimexTradingResults(**arg)
                lines.append(line)
            s.add_all(lines)
            await s.commit()


if __name__ == '__main__':

    SYNC.create_table()

    first_point = time.time()
    SYNC.download()
    print(f'Total time of sync download: {round(time.time() - first_point)} c.')

    parse_excel()

    second_point = time.time()
    SYNC.insert_data()
    print(f'Total time of sync insert: {round(time.time() - second_point)} c.')

    ASYNC.create_table()

    third_point = time.time()
    asyncio.run(ASYNC.download())
    print(f'Total time of async download: {round(time.time() - third_point)} c.')

    parse_excel()

    fourth_point = time.time()
    asyncio.run(ASYNC.insert_data())
    print(f'Total time of async insert: {round(time.time() - fourth_point)} c.')


