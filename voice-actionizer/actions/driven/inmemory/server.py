from actions.driven_port.server import Server


class InMemoryServer(Server):
    def read_book(self, book_author: str) -> str:
        return f'Ok, je vais faire comme si on lisait un livre de {book_author}'

    def play_album(self, artist: str, title: str) -> str:
        return f'Ok, je vais faire comme si on écoutait {title} de {artist}'
