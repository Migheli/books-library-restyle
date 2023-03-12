import argparse
import json
import os
import requests
import urllib3

from requests.exceptions import HTTPError, ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urljoin, urlparse

from tululu import get_page_soup, parse_book_page, \
    download_img, download_txt


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    retry_strategy = Retry(
        total=5,
        backoff_factor=0.1
    )
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    parser = argparse.ArgumentParser(
        description='Program download books from free online-library tululu.org'
    )
    parser.add_argument('-sp', '--start_page', type=int, help='number of the first processed page',
                        default=1)
    parser.add_argument('-ep', '--end_page', type=int, help='number of the last processed page',
                        default=2)
    parser.add_argument('-df', '--dest_folder', type=str,
                        help='folder for saving parser results', default=os.getcwd())
    parser.add_argument('-jp', '--json_path', type=str,
                        help='path to json file with parsing results (without .json extension)',
                        default='books')
    parser.add_argument('-si', '--skip_imgs', action=argparse.BooleanOptionalAction, default=False,
                        help='if this flag is active, images of books are not loaded')
    parser.add_argument('-st', '--skip_txt', action=argparse.BooleanOptionalAction, default=False,
                        help='if this flag is active, texts of books are not loaded')
    args = parser.parse_args()

    all_book_links = []
    for page in range(args.start_page, args.end_page):
        try:
            target_url = f'https://tululu.org/l55/{page}'
            soup = get_page_soup(target_url, session)
            book_cards = soup.select(' .d_book .bookimage a')
            base_url = 'https://tululu.org/'
            book_links = [urljoin(base_url, book_card.get('href')) for book_card in book_cards]
            all_book_links += book_links
        except HTTPError:
            print(f'Error while handling page number {page}. Page skipped.')
        except ConnectionError:
            print('Connection error. Retry...')

    books = []

    for book_link in all_book_links:
        os.chdir(os.path.normpath(args.dest_folder))
        prefix, book_id = urlparse(book_link).path.replace('/', '').split('b')
        soup = get_page_soup(book_link, session)
        book = parse_book_page(soup)
        try:
            if not args.skip_txt:
                os.makedirs('books', exist_ok=True)
                download_txt(book_id, session, book['path'])
            if not args.skip_imgs:
                os.makedirs('img', exist_ok=True)
                download_img(urljoin(book_link, book['img_src']), session)
            books.append(book)
        except HTTPError:
            print(f'Error while handling book with id {book_id}. Skipping download.')
        except ConnectionError:
            print('Connection error. Retrying...')

    books_json = json.dumps(books, ensure_ascii=False)
    with open(f'{os.path.normpath(args.json_path)}.json', 'w') as books_file:
        books_file.write(books_json)


if __name__ == "__main__":
    main()
