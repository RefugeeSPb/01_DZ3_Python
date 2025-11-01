import pytest
import json
from unittest.mock import patch

from scraper import get_book_data, scrape_books


def test_get_book_data_dict():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert isinstance(book_data, dict)



def test_get_book_data_check():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert "name" in book_data


def test_get_book_data_str():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert isinstance(book_data["name"], str)

    
def test_get_book_data_len():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)   
    assert len(book_data) == 9


def test_scrape_books():
    print("Start test_scrape_books")
    
    with open("artifacts/books_data.txt", "r") as f:
        real_data = json.load(f)
    
    with patch("scraper.get_book_data") as mock_get_book_data:
        mock_get_book_data.side_effect = real_data
        result = scrape_books(True, "http://books.toscrape.com/catalogue/page-{N}.html")
        assert result == real_data
        assert isinstance(result, list)
        assert len(result) == 1000