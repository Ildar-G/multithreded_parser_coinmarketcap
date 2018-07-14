"""План
1. Один поток
2. Замер времеи работы
3. Мультипроцессинг
4. Замер
5. Экспорт в cvs"""


import requests
import json
import lxml
import csv

from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool



def get_all_links(html):
    # создаем объект супа и вытаскиваем ссылки в лист links
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id = 'currencies-all').find_all('td', class_='currency-name') #нашли все объекты супа
    links = []

    # итерируем объекты супа и записываем в лист
    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='details-panel-item--name').text.strip()
    except:
        name = ''

    try:
        price = soup.find('span', id = 'quote_price').text.strip()
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('coinmarketcap_3.csv', 'a') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], 'parsed')

def make_all(url):
    page_html = get_html(url)
    page_data = get_page_data(page_html)
    write_csv(page_data)


def get_html(url):
    # get запрос url и получение текста html
    r = requests.get(url) # ответ сервера
    text = r.text # возвращает текст
    return text


def save_txt(url):
    #сохраняет  html в txt - ascii пропускает символы не ascii символы
    with open('text_html.txt', 'a') as file:
        file.write(ascii(get_html(url)))


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'
    html = get_html(url)
    all_links = get_all_links(html) #получаем все ссылки листом

    # for index, link in enumerate(all_links): # для каждой ссылки вытаскиваем хтмл вытаскиваем данные и оохраняем
    #     page_html = get_html(link)
    #     page_data = get_page_data(page_html)
    #     write_csv(page_data)
    #
    #     print(index)

    with Pool(40) as p:
        p.map(make_all, all_links)
    end = datetime.now()



if __name__ == '__main__':
    main()