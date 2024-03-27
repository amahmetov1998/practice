import requests
from bs4 import BeautifulSoup


def parse_html():
    storage_number = 1
    webpage_url = f'https://spimex.com/markets/oil_products/trades/results/'

    while storage_number <= 30:
        response = requests.get(f'{webpage_url}?page=page-{storage_number}').text
        soup = BeautifulSoup(response, 'lxml')
        block = soup.find('div', class_='accordeon-inner')
        all_links = block.find_all('div', class_='accordeon-inner__header')
        all_data = block.find_all('span')

        for i, link in enumerate(all_links):
            download_url = link.find('a').get('href')
            download_link = requests.get(f'https://spimex.com/{download_url}')
            with open(f'files/{storage_number}_{all_data[i].string}.xlsx', 'wb') as f:
                f.write(download_link.content)
        storage_number += 1
