from ner.driven_port.answerer import Answerer


class InMemoryAnswerer(Answerer):
    def answer(self, message: str):
        print(message)
