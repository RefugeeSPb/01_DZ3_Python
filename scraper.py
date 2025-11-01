import os
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

     аргументы:
     book_url (str): ссылка на определенный сайт с книгой в формате str

     return:
     dict: словарь с данными о книге

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
        timeout = (7, 11)
        req_book = requests.get(book_url, timeout=timeout)
        req_book.raise_for_status()
    except req_book.HTTPError as err:  # type: ignore
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
    book_name = req_book_html.find("h1").text.strip()  # type: ignore
    book_dict.update({"name": str(book_name)})

    # 2. Заранее определяем, что p - цена книги. Ищем и вставляем название в словарь
    book_price = req_book_html.find("p", class_="price_color").text.strip()[1:]  # type: ignore
    book_dict.update({"price euro": float(book_price)})

    # 3. Рейтинг (ищем элемент с классом star-rating и извлекаем подкласс)
    rating_element = req_book_html.find("p", class_="star-rating")
    rating_classes = list(rating_element.get("class", []))  # type: ignore
    book_dict.update({"rating": float(rating_book.get(rating_classes[1]))})  # type: ignore

    # 4. Остатки (ищем элемент с классом p - instock availability извлекаем позиции чисел)
    stock_element_start = (
        req_book_html.find("p", class_="instock availability").text.strip().find("(")  # type: ignore
        + 1
    )
    stock_element_end = (
        req_book_html.find("p", class_="instock availability")
        .text.strip()  # type: ignore
        .find(" available")
    )
    # print(req_book_html.find("p", class_="instock availability").text.strip()[stock_element_start:stock_element_end])
    book_dict.update(
        {
            "stock": int(
                req_book_html.find("p", class_="instock availability").text.strip()[  # type: ignore
                    stock_element_start:stock_element_end
                ]
            )
        }
    )

    # 5. Описание (ищем элемент с классом star-rating и извлекаем подкласс)
    try:
        description_element = (
            req_book_html.find("div", id="product_description")
            .find_next("p")  # type: ignore
            .text.strip()  # type: ignore
        )
        book_dict.update({"Decription": str(description_element)})
    except:  # noqa: E722
        book_dict.update({"Decription": "No description"})

    # 6. Product Information. По всем строкам table/tr ищем по th - key, по td - value.
    product_info_element_key = (
        req_book_html.find("h2", string="Product Information")  # type: ignore
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


def scrape_books(is_save: bool, pages_url: str, directory_save: str):
    """
    Функция для получения данных о книгах на определенном сайте

    Функция должна искать ссылки на все страницы книг
    далее при помощи функции get_book_data собрать данные о каждой книге и вернуть их.
    Если сайт оканчивается (ошибка 404), то функция останавливается.
    В случае если is_save == True, сохраните данные в JSON файл.

    В итоге возвращает список книг с такими данными:
    - Название
    - Цена
    - Рейтинг
    - Количество в наличии
    - Описание
    - Дополнительные характеристики

    Аргументы:
    is_save (bool): если True, то создает файл с нуля и сохраняет в него данные.
    В противном случае - ничего не делает.
    Сохраняет файл artifacts/books_data.txt в формате JSON

    pages_url (str): ссылка на сайт с книгами. Выглядит как шаблон с переменной N - номер страницы.

    directory_save: str
        Путь к директории, в которой будет создан файл с данными о книгах.

    Возвращает:
    list[dict]: список словарей с данными о книгах.

    Пример:
        books = scrape_books(
            is_save=True,
            pages_url="http://books.toscrape.com/catalogue/page-{N}.html"
            directory_save="artifacts"
        )
        print(len(books))

        >>>1000
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    # Стартуем с первой страницы. Готовим первую ссылку
    pages_site = 1
    url_site = pages_url.format(N=pages_site)
    book_list = []
    # Будем парсить сайты, пока на наткнемся на 404 ошибку (51 стр.)
    while True:
        timeout = (7, 11)
        req_pages = requests.get(url_site, timeout=timeout)
        # проверка на ошибку
        if req_pages.status_code == 404:
            break

        # Меняем кодировку
        req_pages.encoding = "utf-8"
        # Парсим данные по html
        req_pages_html = BeautifulSoup(req_pages.text, "html.parser")
        # Определяем секцию, в которой расположены книги
        req_pages_html_find = req_pages_html.find("ol", class_="row").find_all(  # type: ignore
            "article", class_="product_pod"
        )
        book_i = 1
        # Для каждой книги определяем ссылку.
        # Далее вытаскиваем данные по каждой книге по ссылке. Сохраняем в список
        for book_pages in req_pages_html_find:
            book_url = book_pages.find("a").get("href")  # type: ignore
            percent_time = ((pages_site - 1) * 20 + book_i) / (50 * 20) * 100
            print(f"{percent_time:.2f}%", end="\r", flush=True)
            book_list.append(
                get_book_data(f"http://books.toscrape.com/catalogue/{book_url}")
            )
            book_i += 1
        pages_site += 1
        url_site = pages_url.format(N=pages_site)

    # Сохраняем в файл в формате json, если указан True
    if is_save:
        try:
            with open(f"{directory_save}/books_data.txt", "w") as f:
                json.dump(book_list, f, indent=4)
        except FileNotFoundError:
            os.makedirs(directory_save)
            with open(f"{directory_save}/books_data.txt", "w") as f:
                json.dump(book_list, f, indent=4)

    return book_list


if __name__ == "__main__":
    res = scrape_books(
        is_save=True,
        pages_url="http://books.toscrape.com/catalogue/page-{N}.html",
        directory_save="artifacts",
    )
    print(f"Собрано {len(res)} книг")
