from abc import ABC, abstractmethod


class Entrypoint(ABC):

    @abstractmethod
    def instruct(self, command: str):
        pass
