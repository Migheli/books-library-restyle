import argparse
import json
import os
import requests
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError, ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import unquote, urljoin, urlsplit, urlparse

from tululu import check_for_redirect, get_page_soup, parse_book_page, \
    download_img, download_txt



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

    os.makedirs('books', exist_ok=True)
    os.makedirs('img', exist_ok=True)

    all_book_links = []
    for page in range(1, 6):
        try:
            target_url = f'https://tululu.org/l55/{page}'
            soup = get_page_soup(target_url, session)
            book_cards = soup.find_all('table', class_='d_book')

            base_url = 'https://tululu.org/'
            book_links = [urljoin(base_url, book_card.find('a').get('href')) for book_card in book_cards]
            all_book_links += book_links

        except HTTPError:
            print(f'Error during handle page number {page}. Page skipped.')
        except ConnectionError:
            print('Connection error. Retry...')

    print(len(all_book_links))
    books = []

    for book_link in all_book_links:
        try:
            prefix, book_id = urlparse(book_link).path.replace('/', '').split('b')
            print(book_id)
            soup = get_page_soup(book_link, session)
            book = parse_book_page(soup)

            print(f'book === {book}')
            download_img(urljoin(book_link, book['img_src']), session)
            download_txt(book['title'], book_id, session)
            books.append(book)
        except HTTPError:
            print(f'Error while handling book with id {book_id}. Skipping download.')
        except ConnectionError:
            print('Connection error. Retrying...')

    books_json = json.dumps(books, ensure_ascii=False)
    with open('books.json', 'w') as books_file:
        books_file.write(books_json)




if __name__ == "__main__":
    main()
