import requests
import csv
import re
from bs4 import BeautifulSoup as BS

_url = 'https://msz72.ru/catalog/'


def get_catalog_urls():
    response = requests.get(url=_url)
    soup = BS(response.content, 'html.parser')

    catalog = soup.find_all('ul', {'class': 'cat-list'})
    urls = []
    for i in catalog:
        list = i.find_all("li")
        for j in list:
            href = j.find("a").get("href")
            urls.append(href)

    with open('catalog-list-urls.html', 'w') as file:
        for url in urls:
            file.write(f"https://msz72.ru{url}\n")


def get_items_url(file_path):
    urls = []
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    for url in urls_list:
        response = requests.get(url=url)
        soup = BS(response.content, 'lxml')
        try:
            items = soup.find('div', {'class': 'inner'}).find_all('div', {'item'})
            for item in items[:5]:
                href_list = item.find('div', {'class': 'info'}).find('a').get('href')
                urls.append(href_list)
        except Exception as _ex:
            item_href = None

    with open('items_href.csv', 'w', encoding='UTF-8', newline='') as file:
        for url in urls:
            file.write(f"https://msz72.ru{url}\n")


def get_data(file_path):
    furniture_name = []
    clear_furniture_name = []
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    for url in urls_list:
        response = requests.get(url=url)
        soup = BS(response.content, 'lxml')
        try:
            item_name = soup.find('div', {'class': 'inner'}).find_all('div', {'row'})
            for item in item_name:
                description = item.find_all('div', {'info'})
                for href in description:
                    name = href.find('a').getText()
                    furniture_name.append(name)
                    for i in reversed(furniture_name):
                        i = i.strip()
                        clear_furniture_name.append(i)
        except Exception as _ex:
            item_name = None

    with open('items.csv', 'w', encoding='UTF-8', newline='') as file:
        for name in clear_furniture_name:
            file.write(f"{name}\n")


def item_parse(file_path):
    furniture_name = []
    clear_furniture_name = []
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    with open('item.csv', 'w', encoding='UTF-8', newline='') as file:
        head = ['Название', 'Размеры (ШхГхВ)', 'Цвет', 'Производитель', 'Цена']
        writer = csv.writer(file)
        writer.writerow(head)

        for url in urls_list:
            response = requests.get(url=url)
            soup = BS(response.content, 'lxml')
            try:

                response = requests.get(url=url)
                soup = BS(response.content, 'lxml')

                item_page = soup.find('div', {'class': 'catalog-page'})
                props = item_page.find('div', {'class': 'props'})
                name = item_page.find('div', {'class': 'c-promo catalogView'}).find('h1').text
                price = props.find_all('div', {'class': 'row2'})[0].find_next('div').text.replace('руб.', '')
                measurement = props.find(string=re.compile("Размеры")).find_next('div').text
                color = props.find(string=re.compile("Цвет")).find_next('div').text
                supplier = props.find(string=re.compile("Производитель")).find_next('div').text

                result = [name, measurement, color, supplier, price]
                writer.writerow(result)

            except Exception as _ex:
                props = None


def main():
    item_parse('items_href.csv')


if __name__ == "__main__":
    main()
