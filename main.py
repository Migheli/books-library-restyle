import argparse
import os
import requests
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError
from urllib.parse import unquote, urljoin, urlsplit


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def parse_book_page(html_content):

    soup = BeautifulSoup(html_content.text, 'lxml')
    title_tag = soup.find('td', class_='ow_px_td').find('h1')
    title_text, author = title_tag.text.split('::')
    title = title_text.strip()

    genres_span = soup.find('span', class_='d_book')
    genres_tags = genres_span.find_all('a')
    genre_names = [genre.text for genre in genres_tags]

    img_src = soup.find('div', class_='bookimage').find('img')['src']

    comment_tags = soup.find_all('div', class_='texts')
    comments = None
    if comment_tags:
        comments = [comment.find('span', class_='black').text for comment in comment_tags]

    return {
                'title': title,
                'genres': genre_names,
                'img_src': img_src,
                'comments': comments,
            }


def download_txt(title, id, folder='books/'):
    url = f'https://tululu.org/txt.php?id={id}'
    sanitized_filename = f'{id} {sanitize_filename(title)}.txt'
    path = os.path.join(folder, sanitized_filename)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    with open(path, 'w') as file:
        file.write(response.text)


def download_img(img_url, folder='img/'):

    response = requests.get(img_url)
    response.raise_for_status()
    sanitized_filename = unquote(urlsplit(img_url).path)
    sanitized_filepath = os.path.basename(sanitized_filename)
    path = os.path.join(folder, sanitized_filepath)

    with open(path, 'wb') as file:
        file.write(response.content)


def main():

    parser = argparse.ArgumentParser(
        description='Программа скачивает файлы из библиотеки tululu.ru'
    )
    parser.add_argument('-s', '--start_id', type=int, help='ID стартовой книги', default=1)
    parser.add_argument('-e', '--end_id', type=int, help='ID финальной книги', default=11)
    args = parser.parse_args()

    START_ID = args.start_id
    END_ID = args.end_id + 1

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    os.makedirs(('books'), exist_ok=True)
    os.makedirs(('img'), exist_ok=True)


    for id in range(START_ID, END_ID):
        try:
            book_url = f'https://tululu.org/b{id}/'

            response = requests.get(book_url, verify=False)
            response.raise_for_status()
            check_for_redirect(response)

            book_info = parse_book_page(response)
            download_img(urljoin(book_url, book_info['img_src']))
            download_txt(book_info['title'], id)

            #print(f'Скачана книга - {book_info["title"]} ')
            #print(f'Жанр: {book_info["genres"]}')
            #print(f'Комментарии к книге: {book_info["comments"]}')

        except HTTPError:
            print(f'Ошибка при скачивании книги с id {id}. Пропускаем.')


if __name__ == "__main__":
    main()
