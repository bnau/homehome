from domain.driven_port.actionizer import Actionizer


class InMemoryActionizer(Actionizer):
    def read_book(self, book_author: str) -> str:
        return f'Ok, je vais faire comme si on lisait un livre de {book_author}'
