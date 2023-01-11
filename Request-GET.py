# Необходимо выгрузить в CSV-файл наименование, цену и описание товаров
# с каждой страницы сайта https://scrapingclub.com/exercise/list_basic/?page=1,
# а также выгрузить в папку images (папка должна быть в корне проекта) картинку каждого товара.
# Если потребуется, то из CSV-файла запросто можно вытащить данные в таблицу Excel.

from requests import get
from bs4 import BeautifulSoup
from time import sleep
from csv import writer

# Необходимо использовать headers в get-запросах, чтобы обойти защиту сайтов
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}


def get_url() -> str:
    """Фунция по очереди возвращает каждую ссылку с товаром
    со всех 8-ми страниц для последующей обработки"""
    for num in range(1, 2):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={num}'
        response = get(url, headers=headers).text
        sleep(2)
        for i in BeautifulSoup(response, 'lxml').find_all('div', class_='col-lg-4 col-md-6 mb-4'):
            yield 'https://scrapingclub.com' + i.find('a').get('href')


def array() -> tuple:
    """Фунция обрабатывает каждую ссылку из функции get_url и возвращает
     кортеж из наименования, цены, описания и ссылки на картинку товара"""
    for i in get_url():
        response = get(i, headers=headers).text
        soup = BeautifulSoup(response, 'lxml').find('div', class_='card mt-4 my-4')
        name, price = soup.find('h3').text, soup.find('h4').text
        description = soup.find('p', class_='card-text').text
        url_img = soup.find('img', class_="card-img-top img-fluid").get('src')
        yield name, price, description, url_img


def uploading() -> None:
    """Функция создаёт csv-файл data.csv (если файл создан, то добавляет в него строки)
     и добавляет в него наименование, цену и описание товара, а также выгружает картинку
     каждого товара в папку images. Папка должна быть создана заранее в корне проекта"""
    for i in array():
        with open('data.csv', 'a', encoding='utf-8', newline='') as f, \
                open("images\\" + i[-1].split('/')[-1], 'wb') as f1:
            f_writer = writer(f)
            f_writer.writerow(i)
            resp = get('https://scrapingclub.com' + i[-1], stream=True)
            for j in resp:
                f1.write(j)


uploading() # Запускаем программу
