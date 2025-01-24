from typing import List

from ner.driven_port.store import Store


class InMemoryStore(Store):

    def __init__(self, docs: List[str]) -> None:
        self.__docs = docs

    def add(self, doc: str) -> None:
        pass

    def retrieve(self, query: str) -> List[str]:
        return self.__docs
