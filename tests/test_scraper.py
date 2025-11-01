import pytest
import json
from unittest.mock import patch

from scraper import get_book_data, scrape_books


def test_get_book_data():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert isinstance(book_data, dict)
    assert "name" in book_data
    assert isinstance(book_data["name"], str)   
    assert len(book_data) == 9


"""def test_scrape_books(mocker):
    print("Start test_scrape_books")
    
    with open("artifacts/books_data.txt", "r") as f:
        real_data = json.load(f)
    
    with patch("scraper.get_book_data") as mock_get_book_data:
        mock_get_book.return_value = real_data

        result = scrape_books(True, "http://books.toscrape.com/catalogue/page-{N}.html")
        assert result == real_data
        assert isinstance(result, list)
        assert len(result) == 10000"""