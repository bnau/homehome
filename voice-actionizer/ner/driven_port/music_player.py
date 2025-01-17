from abc import ABC, abstractmethod

from actions.model.album import Album


class MusicPlayer(ABC):
    @abstractmethod
    def play(self, album: Album) -> str:
        pass

