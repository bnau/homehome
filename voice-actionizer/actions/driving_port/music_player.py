from abc import ABC, abstractmethod

from actions.driven_port.server import Server
from actions.model.album import Album


class MusicPlayer(ABC):
    @abstractmethod
    def play(self, album: Album) -> str:
        pass


class DomainMusicPlayer(MusicPlayer):
    server: Server

    def __init__(self, server: Server):
        self.server = server

    def play(self, album: Album) -> str:
        return self.server.play_album(album.artist, album.title)
