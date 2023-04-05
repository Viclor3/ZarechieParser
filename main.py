import requests
from bs4 import BeautifulSoup as BS

_url = 'https://msz72.ru/catalog/'
#https://msz72.ru/catalog/gotovye-resheniya/prikhozhie-gotovye/

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
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    for url in urls_list:
        response = requests.get(url=url)
        soup = BS(response.content, 'html.parser')

        try:
            item_name = soup.find_all('div', {'class': 'inner'})
            for item in item_name:
                info_block = item.find('div', {'class': 'info'})
                for furniture in info_block:
                    name = furniture.find('a')
                    furniture_name.append(name)

        except Exception as _ex:
            item_name = None

    print(furniture_name)


def main():
    # get_items_urls()
    get_data(file_path="catalog-list-urls.html")


if __name__ == "__main__":
    main()
