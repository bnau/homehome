from abc import ABC, abstractmethod
from typing import Optional

from actions.driving_port.book_reader import BookReader
from actions.driving_port.music_player import MusicPlayer
from actions.model.album import Album
from actions.model.book import Book
from ner.driven_port.actionizer import Actionizer


class MainActionizer(Actionizer):
    book_reader: BookReader
    music_player: MusicPlayer

    def __init__(self, book_reader: BookReader, music_player: MusicPlayer):
        self.book_reader = book_reader
        self.music_player = music_player

    def read_book(self, author: Optional[str]) -> str:
        return self.book_reader.read(Book(author=author))

    def play_album(self, artist: str, title: str) -> str:
        return self.music_player.play(Album(artist=artist, title=title))
