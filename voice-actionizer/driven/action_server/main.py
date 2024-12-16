from domain.driven_port.actionizer import Actionizer
from requests import post


class ServerActionizer(Actionizer):
    def read_book(self, book_author: str) -> str:
        response = post('http://localhost:3000', json={'next_action': 'action_play_audio_book', 'author': book_author})
        return response.text
    
    def play_album(self, artist: str, title: str) -> str:
        pass

