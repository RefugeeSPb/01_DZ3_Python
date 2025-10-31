import datetime
import requests
import json
from bs4 import BeautifulSoup

# import pytest
# import schedule
# import time


def get_book_data(book_url: str) -> dict:
    """
    Функция для получения данных о книге по url

    Функция должна возвращать определенную информацию по книге:
    - Название
    - Цена
    - Рейтинг
    - Количество в наличии
    - Описание
    - Дополнительные характеристики

    Функция должна возвращать словарь в формате словаря:
    {
        'name': 'Название книги',
        'price euro': 'Цена',
        'rating': 'Рейтинг',
        'stock': 'Количество в наличии',
        'description': 'Описание',
        'Product Information': 'Дополнительные характеристики'  --Данные список будет выводится по всем возможным дополнительным параметрам
     }

     аргументы: ссылка на книгу в формате str

      методы:
      pass

     return: словарь с данными о книге

    >>>book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    >>>get_book_data(book_url)

        {'name': 'A Light in the Attic',
        'price euro': 51.77,
        'rating': 3.0,
        'stock': 22,
        'Decription': "It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more",
        'UPC': 'a897fe39b1053632',
        'Product Type': 'Books',
        'Tax': 0.0,
        'Number of reviews': '0'}
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    # Создаем словарь с ключами
    book_dict = {}
    # Перевод рейтинга в числа
    rating_book = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    # список дополнительных данных, которые мы не выгружаем, так как уже подобные есть
    book_exception_description = {
        "Price (excl. tax)",
        "Price (incl. tax)",
        "Availability",
    }

    # Получаем данные о книге. Проверяем подключение
    try:
        req_book = requests.get(book_url)
        req_book.raise_for_status()
        timeout = (7, 11)  # noqa: F841
    except req_book.HTTPError as err: # type: ignore
        return print(f"Возникла ошибка: {err}")  # type: ignore # надо ли вообще?

    # Имеем HTML формат. Так как мы парсим опредлеленный сайт, то мы не проверяем тип данных
    # print(req_book.headers["Content-Type"])

    # Проверяем кодировку
    # current_encoding = req_book.encoding
    # print(f"Текущая кодировка: {current_encoding}")
    req_book.encoding = "utf-8"

    # Парсим данные по html
    req_book_html = BeautifulSoup(req_book.text, "html.parser")

    # 1. Заранее определяем, что h1 - название книги. Ищем и вставляем название в словарь
    book_name = req_book_html.find("h1").text.strip() # type: ignore
    book_dict.update({"name": str(book_name)})

    # 2. Заранее определяем, что p - цена книги. Ищем и вставляем название в словарь
    book_price = req_book_html.find("p", class_="price_color").text.strip()[1:] # type: ignore
    book_dict.update({"price euro": float(book_price)})

    # 3. Рейтинг (ищем элемент с классом star-rating и извлекаем подкласс)
    rating_element = req_book_html.find("p", class_="star-rating")
    rating_classes = list(rating_element.get("class", []))  # type: ignore
    book_dict.update({"rating": float(rating_book.get(rating_classes[1]))})  # type: ignore

    # 4. Остатки (ищем элемент с классом p - instock availability извлекаем позиции чисел)
    stock_element_start = (
        req_book_html.find("p", class_="instock availability").text.strip().find("(") # type: ignore
        + 1
    )
    stock_element_end = (
        req_book_html.find("p", class_="instock availability")
        .text.strip() # type: ignore
        .find(" available")
    )
    # print(req_book_html.find("p", class_="instock availability").text.strip()[stock_element_start:stock_element_end])
    book_dict.update(
        {
            "stock": int(
                req_book_html.find("p", class_="instock availability").text.strip()[ # type: ignore
                    stock_element_start:stock_element_end
                ]
            )
        }
    )

    # 5. Описание (ищем элемент с классом star-rating и извлекаем подкласс)
    try:
        description_element = (
            req_book_html.find("div", id="product_description")
            .find_next("p") # type: ignore
            .text.strip() # type: ignore
        )
        book_dict.update({"Decription": str(description_element)})
    except:  # noqa: E722
        book_dict.update({"Decription": "No description"})

    # 6. Product Information. По всем строкам table/tr ищем по th - key, по td - value.
    product_info_element_key = (
        req_book_html.find("h2", string="Product Information") # type: ignore
        .find_next("table")
        .find_all("tr")
    )

    for row in product_info_element_key:
        try:
            key = row.find("th").text.strip()
            if key in book_exception_description:
                continue
            value = row.find("td").text.strip()
            #
            book_dict[key] = value if key != "Tax" else float(value[1:])
        except:  # noqa: E722
            continue
        # pass

    return book_dict
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ


def scrape_books(is_save: bool, pages_url: str):
    """
    МЕСТО ДЛЯ ДОКУМЕНТАЦИИ
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    # http://books.toscrape.com/catalogue/page-{N}.html
    # http://books.toscrape.com/catalogue/page-1.html
    # http://books.toscrape.com/catalogue/page-51.html     51 страница - 404

    # Стартуем с первой страницы
    pages_site = 1
    # url_site = f"http://books.toscrape.com/catalogue/page-{pages_site}.html"
    url_site = pages_url.format(N=pages_site)
    book_list = []
    # Пока не выпадем в ошибку
    while True:
        # while pages_site <= 3:
        req_pages = requests.get(url_site)
        # print(url_site)
        timeout = (7, 11)  # noqa: F841
        # проверка на ошибку
        if req_pages.status_code == 404:
            break

        req_pages.encoding = "utf-8"
        req_pages_html = BeautifulSoup(req_pages.text, "html.parser")
        # print(req_pages_html.prettify())
        req_pages_html_find = req_pages_html.find("ol", class_="row").find_all( # type: ignore
            "article", class_="product_pod"
        )
        # print(req_pages_html_find)
        book_i = 1
        # book_list = []
        for book_pages in req_pages_html_find:
            book_url = book_pages.find("a").get("href") # type: ignore
            # print(f"Page:{pages_site}, №{book_i}. URL: {book_url}")
            percent_time = ((pages_site - 1) * 20 + book_i) / (50 * 20) * 100
            print(f"{percent_time:.2f}%", end="\r", flush=True)
            book_list.append(
                get_book_data(f"http://books.toscrape.com/catalogue/{book_url}")
            )
            book_i += 1

        # print(book_list)

        pages_site += 1
        url_site = pages_url.format(N=pages_site)
        # url_site = f"http://books.toscrape.com/catalogue/page-{pages_site}.html"

    if is_save:
        with open("books_data.txt", "w") as f:
            f.write("")
        for book in book_list:
            with open("books_data.txt", "a") as f:
                json.dump(book, f, indent=4)

    print(datetime.datetime.now())
    return book_list


if __name__ == "__main__":
    res = scrape_books(True, "http://books.toscrape.com/catalogue/page-{N}.html")
    print(res)


if __name__ == "__main__":
    book_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    get_book_data(book_url)
