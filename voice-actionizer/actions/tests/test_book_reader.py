from actions.driven.inmemory.server import InMemoryServer
from actions.driving.book_reader import DomainBookReader
from actions.model.book import Book


def test_book_reader_should_acknowledge_book_reading_with_author():
    server = InMemoryServer()

    book_reader = DomainBookReader(server)

    assert book_reader.read(Book(author="Chateaubriand")) == ("Ok, je vais faire comme si on lisait un livre de "
                                                              "Chateaubriand")
