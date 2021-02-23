import csv
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from data_base import db

user_agent = UserAgent()
base_url = "https://stomshop.pro/"
menu_url = base_url + "stomatologicheskoye-oborudovaniye/"
count = 1
headers = {"user-agent": user_agent.random}


def get_response(url, **kwargs):
    """- Получить ответ запросы по ссылке"""
    time.sleep(0.01)

    global count, headers
    count += 1

    if count == 10:
        headers = {"user-agent": user_agent.random}

    with requests.Session() as session:
        response = session.get(url=url, headers=headers, params=kwargs)
        if response.ok:
            return response
        else:
            print('ОШИБКА - 404')


def get_all_links(text):
    """- Получить ве ссылки"""
    links = []
    soup = BeautifulSoup(text, "lxml")
    menu = soup.find("div", {"class": "yum-am"}).ul
    for li in menu.find_all("li"):
        link = li.find("a", {"class": "item-wrapper"}).get("href")
        if link:
            links.append(link)
    return links


def get_paginate(text):
    """- Получить количество пагинации"""
    try:
        soup = BeautifulSoup(text, "lxml")
        pagination = soup.find("div", {"class": "row paginator"}).find("div", {"class": "col-sm-6 text-right"}).text
        return pagination.split()[-2]
    except Exception as e:
        print(f"Пгинация отсутствуе {e}")
        return None


def get_links_products(text):
    """- Получить количество пагинации"""
    links = []
    try:
        soup = BeautifulSoup(text, "lxml")
        products = soup.find("div", {"class": "row products"}).find_all("div", {"class": "caption"})
        for product in products:
            link = product.a.get("href")
            if link:
                links.append(link)
    except Exception as e:
        print(f"Это статья или данные на странице отсутствуют {e}")

    return links


def csv_writer(data):
    """Функция для записи данных в CSV"""
    with open("links_product.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow([row])


def main():
    menu_response = get_response(menu_url)
    links = get_all_links(menu_response.text)

    print(links)

    for link in links:

        print(link)

        page_response = get_response(link, **dict(limit=100))
        number_page = get_paginate(page_response.text)

        print(number_page)

        links_products = []

        if not number_page:
            print("ok")
            links = get_links_products(page_response.text)
            links_products.extend(links)

        else:
            for i in range(1, int(number_page) + 1):
                page_response = get_response(link, **dict(limit=100, page=i))
                links = get_links_products(page_response.text)
                links_products.extend(links)

        print(len(links_products))
        print(links_products)

        csv_writer(links_products)


if __name__ == '__main__':
    main()

