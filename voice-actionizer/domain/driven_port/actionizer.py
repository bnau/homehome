from abc import ABC, abstractmethod


class Actionizer(ABC):

    @abstractmethod
    def read_book(self, book_author: str) -> str:
        pass
