from abc import ABC, abstractmethod


class Answerer(ABC):

    @abstractmethod
    def answer(self, message: str):
        pass
