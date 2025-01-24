from abc import ABC, abstractmethod
from typing import List


class Store(ABC):

    @abstractmethod
    def add(self, doc: str) -> None:
        pass

    @abstractmethod
    def retrieve(self, query: str) -> List[str]:
        pass
