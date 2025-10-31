import pytest
from main import get_book_data, scrape_books


def test_get_book_data():
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert isinstance(book_data, dict)
    assert "name" in book_data
    assert isinstance(book_data["name"], str)   
    assert len(book_data) == 9