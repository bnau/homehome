from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.driving_port.entrypoint import Entrypoint
from domain.intention import Intention


class Instructor(Entrypoint):
    actionizer: Actionizer
    answerer: Answerer

    def __init__(self, actionizer: Actionizer, answerer: Answerer):
        self.actionizer = actionizer
        self.answerer = answerer

    def instruct(self, command: str):
        Intention(self.actionizer, self.answerer).actionize(command)
