from abc import ABC, abstractmethod
from typing import Optional


class Actionizer(ABC):
    @abstractmethod
    def read_book(self, author: Optional[str]) -> str:
        pass

    @abstractmethod
    def play_album(self, artist: str, title: str) -> str:
        pass
