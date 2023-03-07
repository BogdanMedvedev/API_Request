# Необходимо выполнить авторизацию с произвольными данными
# на тестовом сайте http://quotes.toscrape.com

from requests import Session
from bs4 import BeautifulSoup

# Необходимо использовать headers в get и post запросах, чтобы обойти защиту сайтов
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

# Создаём сессию, чтобы работать в рамках одной сессии, сохраняя файлы cookie
work = Session()

# Переходим на сайт в рамках сессии
work.get('https://quotes.toscrape.com', headers=headers)

# Переходим на страницу авторизации
response = work.get('https://quotes.toscrape.com/login', headers=headers).text

# Создаём элемент BeautifulSoup, чтобы было удобнее выполнять поиск по странице
soup = BeautifulSoup(response, 'lxml')

# Вытаскиваем из сессии токен и сохраняем в переменную для дальнейшей авторизации
token = soup.find('input', type='hidden').get('value')

# Создаём словарь с данными для последующей авторизации
data = {'csrf_token': token, 'username': 1234, 'password': 1234}

# Выполняем авторизацию на сайте, атрибут "allow_redirects" позволяет разрешить перенаправление, если оно есть
result = work.post('https://quotes.toscrape.com/login', headers=headers, data=data, allow_redirects=True)

# Убедимся, что вход выполнен, найдя на странице "Logout" (оно появляется только после атворизации)
print(BeautifulSoup(result.text, 'lxml').find('div', class_='col-md-4').text.replace('\n',''))