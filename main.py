import os
import requests
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError
from urllib.parse import unquote, urljoin, urlsplit

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




def check_for_redirect(response):
    if response.history:
        raise HTTPError

#MAIN_PAGE_URL = 'https://tululu.org/'

def get_filename(book_url, book_id):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('td', class_='ow_px_td').find('h1')
    title_text, author = title_tag.text.split('::')
    striped_title_text = title_text.strip()

    return f'{book_id}. {striped_title_text}.txt'



def download_txt(url, filename, folder='books/'):

    sanitized_filename = f'{sanitize_filename(filename)}.txt'
    path = os.path.join(folder, sanitized_filename)
    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(path, 'w') as file:
        file.write(response.text)
    return path

def download_img(book_url, folder='img/'):

    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    img_src = soup.find('div', class_='bookimage').find('img')['src']

    img_url = urljoin(book_url, img_src)

    response = requests.get(img_url)
    response.raise_for_status()

    sanitized_filename = unquote(urlsplit(img_url).path)
    sanitized_filename = os.path.basename(sanitized_filename)


    path = os.path.join(folder, sanitized_filename)
    comments = soup.find_all('div', class_='texts')
    if comments:
        for comment in comments:
            comment_text = comment.find('span', class_='black').text
            print(comment_text)

    with open(path, 'wb') as file:
        file.write(response.content)
    return path


os.makedirs(('books'),  exist_ok=True)
os.makedirs(('img'),  exist_ok=True)

for id in range(1, 11):
    book_file_url = f'https://tululu.org/txt.php?id={id}'
    book_description_url = f'https://tululu.org/b{id}'
    file_response = requests.get(book_file_url, verify=False)
    description_response = requests.get(book_description_url, verify=False)
    try:
        check_for_redirect(file_response)
        description_response.raise_for_status()
        download_txt(book_file_url, get_filename(book_description_url, id))
        download_img(book_description_url)
    except HTTPError:
        print('АЯ-ЯЙ! Ошибка')

