import asyncio

import aiofiles
import aiohttp
import pandas as pd
import requests

dates = pd.date_range(start='2023/01/10', end='2024/04/12')


def sync_download_file():
    for date in dates:
        date = date.strftime('%Y%m%d')
        url = f'https://spimex.com/upload/reports/oil_xls/oil_xls_{date}162000'
        with open(f'files/{date}.xlsx', 'wb') as f:
            link = requests.get(url)
            f.write(link.content)


async def async_download_file(session, date, link):
    async with session.get(link) as response:
        async with aiofiles.open(f'files/{date}.xlsx', 'wb') as fp:
            await fp.write(await response.read())


async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for date in dates:
            date = date.strftime('%Y%m%d')
            link = f'https://spimex.com/upload/reports/oil_xls/oil_xls_{date}162000'
            task = asyncio.create_task(async_download_file(session, date, link))
            tasks.append(task)
        await asyncio.gather(*tasks)
