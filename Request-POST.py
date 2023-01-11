# Необходимо выполнить авторизацию с произвольными данными
# на тестовом сайте http://quotes.toscrape.com с произвольными данными

from requests import Session
from bs4 import BeautifulSoup

# Необходимо использовать headers в get и post запросах, чтобы обойти защиту сайтов
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

# создаём сессию, чтобы работать в рамках одной сессии, сохраняя файлы cookie
work = Session()

# заходим на сайт
work.get('https://quotes.toscrape.com', headers=headers)

# заходит на страницу авторизации
response = work.get('https://quotes.toscrape.com/login', headers=headers).text

# создаём элемент BeautifulSoup, чтобы удобнее делать поиск по странице
soup = BeautifulSoup(response, 'lxml')

# вытаскиваем токен и сохраняем в переменную для дальнейшей авторизации
token = soup.find('input', type='hidden').get('value')

# создаём словарь с данными для авторизации
data = {'csrf_token': token, 'username': 1234, 'password': 1234}

# проходим авторизацию на сайте, атрибут allow_redirects позволяет разрешить перенаправление
result = work.post('https://quotes.toscrape.com/login', headers=headers, data=data, allow_redirects=True)

# убедимся, что вход выполнен, найдя на странице "Logout"
print(BeautifulSoup(result.text, 'lxml').find('div', class_='col-md-4').text.replace('\n',''))