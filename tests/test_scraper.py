import pytest
import json

from scraper import get_book_data, scrape_books


def test_get_book_data():
    print("Start test_get_book_data")
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    book_data = get_book_data(book_url)
    assert isinstance(book_data, dict)
    assert "name" in book_data
    assert isinstance(book_data["name"], str)   
    assert len(book_data) == 9


def test_scrape_books(mocker):
    print("Start test_scrape_books")
    mocker.patch(
            "scraper.get_book_data",
            return_value={"name": "Test Book", "price": "£5.00"}
        )
    assert