import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3

quotes = []
authors = []
links = []

n_pages = 0
for page in range(0, 11):
    n_pages += 1
    url = f'https://quotes.toscrape.com/page/{page}'
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    divs = soup.find_all('div', class_='quote')

    for div in divs:
        quote = div.find('span', class_='text').get_text(strip=True)
        quotes.append(quote)
        author = div.find('small', class_='author').get_text(strip=True)
        authors.append(author)
        link = div.find('a', href=True).get('href')
        links.append(link)
print(len(quotes))
print(len(authors))
print(len(links))

cols = ['quote', 'author', 'link']
table = pd.DataFrame({'quote': quotes,
                      'author': authors,
                      'link': links})[cols]

conn = sqlite3.connect('lb1.db')
cursor = conn.cursor()


def create_table():
    query = cursor.execute("""CREATE TABLE IF NOT EXISTS quotes(
        quote TEXT,
        author TEXT,
        link TEXT
    )""")
    conn.commit()
    if (query):
        return "Table was created!"
    else:
        return "Something went wrong!"


def add_data(df):
    add = df.to_sql('quotes', conn, if_exists='replace')
    if (add):
        print("Данные успешно добавлены")

    return add
