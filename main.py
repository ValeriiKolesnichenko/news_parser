"""This program parses all the latest news from korrespondent.net with description."""
import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

url = 'https://ua.korrespondent.net/'
req = requests.get(url=url, headers=headers)
req.encoding = 'utf-8'
data = req.text


with open('news_data.html', 'w', encoding='utf-8') as file:
    file.write(data)

with open('news_data.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# Getting the whole article
articles = soup.find_all('div', class_="article")
# Retrieving news data
for article in articles:
    try:
        article_time = article.find('div', class_='article__time')
        article_title = article.find('div', class_='article__title')
        article_url = article.find('div', class_='article__title').find('a').get('href')

        if article_time and article_title and article_url:
            # Retrieving data by each link
            url_req = requests.get(url=article_url, headers=headers)
            url_req.encoding = 'utf-8'
            article_description = url_req.text
            soup = BeautifulSoup(article_description, 'lxml')
            get_description = soup.find('div', class_='post-item__text').text.strip()
            print(f'{article_time.text}\n'
                  f'{article_title.text}\n'
                  f'{get_description}\n')
            print('*' * 50)
    except Exception as e:
        print('Some trouble here')
        print('*' * 50)

# I don't see any reasons for creating some files to save this data
