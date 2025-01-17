from abc import ABC, abstractmethod

from actions.driven_port.server import Server
from actions.model.book import Book


class BookReader(ABC):
    @abstractmethod
    def read(self, book: Book) -> str:
        pass


class DomainBookReader(BookReader):
    server: Server

    def __init__(self, server: Server):
        self.server = server

    def read(self, book: Book) -> str:
        return self.server.read_book(book.author)
