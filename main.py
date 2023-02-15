import os

import requests
from requests import HTTPError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_for_redirect(response):
    if response.history:
        raise HTTPError

os.makedirs(('books'),  exist_ok=True)
for id in range(1, 11):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url, verify=False)
    try:
        check_for_redirect(response)
        response.raise_for_status()
        filename = f'id{id}.txt'
        with open(f'books/{filename}', 'w') as file:
            file.write(response.text)
    except HTTPError:
        print('АЯ-ЯЙ! Ошибка')
