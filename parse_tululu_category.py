import argparse
import os
import requests
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError, ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import unquote, urljoin, urlsplit

from tululu import check_for_redirect, get_page_soup



def main():

    retry_strategy = Retry(
        total=5,
        backoff_factor=0.1
    )
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    parser = argparse.ArgumentParser(
        description='Program download books from free online-library tululu.org'
    )
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    total_links = []
    for page in range(1, 11):
        try:
            target_url = f'https://tululu.org/l55/{page}'
            soup = get_page_soup(target_url, session)
            book_cards = soup.find_all('table', class_='d_book')

            base_url = 'https://tululu.org/'
            book_links = [urljoin(base_url, book_card.find('a').get('href')) for book_card in book_cards]
            total_links += book_links

        except HTTPError:
            print(f'Error during handle page number {page}. Skip it.')
        except ConnectionError:
            print('Connection error. Try one more time.')

    print(total_links)
if __name__ == "__main__":
    main()
