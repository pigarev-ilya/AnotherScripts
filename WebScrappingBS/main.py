import requests
from bs4 import BeautifulSoup
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
page = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(page.text, 'html.parser')
articles = soup.find_all('article')

for article in articles:
    for keyword in KEYWORDS:
        if keyword in article.text:
            time = article.find('time')
            title = article.find('h2')
            link = title.find('a').attrs.get('href')
            print(f"{time.text} - {title.text} - {'https://habr.com' + link}")
            break


for article in articles:
    title = article.find('h2')
    time = article.find('time')
    link_full_article = 'https://habr.com' + title.find('a').attrs.get('href')
    full_article_page = requests.get(link_full_article)
    soup_full_article = BeautifulSoup(full_article_page.text, 'html.parser')
    full_article = soup_full_article.find('article')
    for keyword in KEYWORDS:
        if keyword in full_article.text:
            print(f"{time.text} - {title.text} - {link_full_article}")
            break

