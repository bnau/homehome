from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer


class Intention:
    actionizer: Actionizer
    answerer: Answerer

    def __init__(self, actionizer: Actionizer, answerer: Answerer):
        self.actionizer = actionizer
        self.answerer = answerer

    def actionize(self, param: str):
        self.answerer.answer(self.actionizer.read_book(param))
