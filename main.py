import requests
from bs4 import BeautifulSoup as BS

_url = 'https://msz72.ru/catalog/'


def get_items_urls():
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
                    for i in furniture_name:
                        i = i.strip()
                        clear_furniture_name.append(i)
        except Exception as _ex:
            item_name = None

    with open('catalog-items.csv', 'w', encoding='UTF-8', newline='') as file:
        for name in clear_furniture_name:
            file.write(f"{name}\n")


def main():
    # get_items_urls()
    get_data(file_path="catalog-list-urls.html")


if __name__ == "__main__":
    main()
