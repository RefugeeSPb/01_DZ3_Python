import pytest # нужен для декоратора skip
import json
import inspect
from unittest.mock import patch
from scraper import get_book_data, scrape_books


"""
    ######################################
    Зона начала тестирования get_book_data 
    ######################################
"""

""" Setup_book_url """
book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
book_data = get_book_data(book_url)



"""Тест для проверки, что функция возвращает словарь"""
#@pytest.mark.skip(reason="Тестирование функции scape_books")
def test_get_book_data_dict():
    print(f"Start {inspect.currentframe().f_code.co_name}", end="\n") # type: ignore
    assert isinstance(book_data, dict)



"""Тест для проверки наличия ключа "name" в словаре"""
#@pytest.mark.skip(reason="Тестирование функции scape_books")
def test_get_book_data_check():
    print(f"Start {inspect.currentframe().f_code.co_name}", end="\n") # type: ignore
    assert "name" in book_data


"""Тест для проверки типа значения ключа "name" в словаре"""
#@pytest.mark.skip(reason="Тестирование функции scape_books")
def test_get_book_data_str():
    print(f"Start {inspect.currentframe().f_code.co_name}", end="\n") # type: ignore
    assert isinstance(book_data["name"], str)


"""Тест для проверки длины словаря"""
#@pytest.mark.skip(reason="Тестирование функции scape_books")
def test_get_book_data_len():
    print(f"Start {inspect.currentframe().f_code.co_name}", end="\n") # type: ignore
    assert len(book_data) == 9


"""
    Зона окончания тестирования get_book_data 
"""


"""
    #####################################
    Зона начала тестирования scrape_books
    #####################################
"""
"""Создаем данные для проверки"""
with open("artifacts/books_data.txt", "r") as f:
    real_data = json.load(f)

"""Создаем мок-функцию"""
with patch("scraper.get_book_data") as mock_get_book_data:
    mock_get_book_data.side_effect = real_data
    result = scrape_books(is_save = True, pages_url="http://books.toscrape.com/catalogue/page-{N}.html", directory_save="artifacts")


"""тестирование, что ожидаем определенный список данных"""
# @pytest.mark.skip(reason="Тестирование функции get_book_data")
def test_scrape_books_data():
    print(f"Start {inspect.currentframe().f_code.co_name}", end="\n") # type: ignore
    assert result == real_data

"""тестирование, что функция возвращает список"""
#@pytest.mark.skip(reason="Тестирование функции get_book_data")
def test_scrape_books_list():
    print(f"Start {inspect.currentframe().f_code.co_name}/n") # type: ignore
    assert isinstance(result, list)

"""тестирование, что функция возвращает список длиной 1000"""
#@pytest.mark.skip(reason="Тестирование функции get_book_data")
def test_scrape_books_len():
    print(f"Start {inspect.currentframe().f_code.co_name}/n") # type: ignore
    assert len(result) == 1000


"""
    Зона окончания тестирования scrape_books
"""