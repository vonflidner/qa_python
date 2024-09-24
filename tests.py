import pytest


class TestBooksCollector:

    @pytest.mark.parametrize("book_name, expected", [
        ("Гордость и предубеждение и зомби", True),
        ("Что делать, если ваш кот хочет вас убить", True),
        ("", False),
        ("Книга" * 20, False),
    ])
    def test_add_new_book(self, collector, book_name, expected):
        collector.add_new_book(book_name)
        assert expected == (book_name in collector.get_books_genre())

    def test_new_book_has_no_genre(self, collector):
        collector.add_new_book("Капитал")
        assert collector.get_book_genre("Капитал") == ""

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Будущее"]),
        ("Детективы", ["Пуаро"]),
        ("Комедии", [])
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books):
        collector.add_new_book("Будущее")
        collector.add_new_book("Пуаро")
        collector.set_book_genre("Будущее", "Фантастика")
        collector.set_book_genre("Пуаро", "Детективы")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    @pytest.mark.parametrize("book_name, genre, expected_genre", [
        ("Будущее", "Фантастика", "Фантастика"),
        ("Пуаро", "Детективы", "Детективы"),
        ("Пуаро", "Поэзия", ""),
        ("Буратино", "Мультфильмы", "Мультфильмы")
    ])
    def test_set_book_genre(self, collector, book_name, genre, expected_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize("book_name, genre, expected_books_for_children", [
        ("Маугли", "Мультфильмы",["Маугли"]),
        ("Чакки", "Ужасы", [])
    ])
    def test_get_books_for_children(self, collector, book_name, genre, expected_books_for_children):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_books_for_children() == expected_books_for_children

    @pytest.mark.parametrize("book_name", [
        "Буратино", "Пуаро"
    ])
    def test_add_book_in_favorites(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("book_name", [
        "Буратино", "Пуаро"
    ])
    def test_delete_book_from_favorites(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()

    def test_delete_book_from_empty_favorites(self, collector):
        collector.delete_book_from_favorites("Пуаро")
        assert collector.get_list_of_favorites_books() == []

    def test_age_restricted_books_not_in_children_list(self, collector):
        collector.add_new_book("Чакки")
        collector.set_book_genre("Чакки", "Ужасы")
        assert collector.get_books_for_children() == []