from abc import ABC, abstractmethod


class Server(ABC):

    @abstractmethod
    def read_book(self, book_author: str) -> str:
        pass

    @abstractmethod
    def play_album(self, artist: str, title: str) -> str:
        pass
