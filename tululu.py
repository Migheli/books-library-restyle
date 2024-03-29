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


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def parse_book_page(soup):
    title_tag = soup.select_one('.ow_px_td h1')

    title_text, author = title_tag.text.split('::')
    title = title_text.strip()
    author = author.strip()

    genre_tags = soup.select('span.d_book a')
    genre_names = [genre.text for genre in genre_tags]

    img_src = soup.select_one('.bookimage img')['src']

    comment_tags = soup.select('.texts')
    comments = [comment.select_one('span.black').text for comment in comment_tags]

    path = os.path.join('books', f'{sanitize_filename(title)}.txt')

    return {
                'title': title,
                'author': author,
                'path': path,
                'genres': genre_names,
                'img_src': img_src,
                'comments': comments
           }


def download_txt(id, session, path):
    payload = {'id': id}
    response = session.get('https://tululu.org/txt.php', params=payload, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    with open(path, 'w') as file:
        file.write(response.text)


def download_img(img_url, session, folder='img/'):
    response = session.get(img_url)
    response.raise_for_status()
    sanitized_filename = unquote(urlsplit(img_url).path)
    sanitized_filepath = os.path.basename(sanitized_filename)
    path = os.path.join(folder, sanitized_filepath)

    with open(path, 'wb') as file:
        file.write(response.content)


def get_page_soup(url, session):
    response = session.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def main():

    retry_strategy = Retry(
        total=5,
        backoff_factor=0.1
    )
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    parser = argparse.ArgumentParser(
        description='Программа скачивает файлы из библиотеки tululu.org'
    )
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    parser.add_argument('-s', '--start_id', type=int, help='ID стартовой книги', default=1)
    parser.add_argument('-e', '--end_id', type=int, help='ID финальной книги', default=11)
    args = parser.parse_args()

    os.makedirs('books', exist_ok=True)
    os.makedirs('img', exist_ok=True)

    for book_id in range(args.start_id, args.end_id):
        try:
            book_url = f'https://tululu.org/b{book_id}/'
            soup = get_page_soup(book_url, session)
            book = parse_book_page(soup)
            download_img(urljoin(book_url, book['img_src']), session)
            download_txt(book_id, session, book['path'])

        except HTTPError:
            print(f'Ошибка при скачивании книги с id {book_id}. Пропускаем.')
        except ConnectionError:
            print('Ошибка соединения. Пробуем еще раз.')


if __name__ == "__main__":
    main()
