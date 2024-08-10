from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.model.intention import Intention


class Instructor(ABC):
    @abstractmethod
    def instruct(self, command: str):
        pass


class DomainInstructor:
    actionizer: Actionizer
    answerer: Answerer

    def __init__(self, actionizer: Actionizer, answerer: Answerer):
        self.actionizer = actionizer
        self.answerer = answerer

    def instruct(self, command: str):
        Intention(self.actionizer, self.answerer).actionize(command)
