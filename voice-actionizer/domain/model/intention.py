from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class IntentionFactory(BaseModel):
    intention: Optional[str] = Field(title="Intention", description="Intention to perform",default="")
    author: Optional[str] = Field(title="Author", description="Author of the book",default="")
    title: Optional[str] = Field(title="Title", description="Title of the album",default="")
    artist: Optional[str] = Field(title="Artist", description="Artist of the album",default="")

    def __getitem__(self, key):
        return getattr(self, key)

    def create_intention(self, actionizer: Actionizer, answerer: Answerer):
        if self.intention == "readBook":
            return ReadBookIntention(actionizer, answerer, self.author)
        elif self.intention == "playAlbum":
            return PlayAlbumIntention(actionizer, answerer, self.artist, self.title)
        else:
            raise Exception(f"Unknown intention {self.intention}")


class Intention(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def actionize(self):
        pass


class ReadBookIntention(Intention):
    actionizer: Actionizer
    answerer: Answerer
    author: Optional[str]

    def __init__(self, actionizer: Actionizer, answerer: Answerer, author: Optional[str]):
        super().__init__()
        self.actionizer = actionizer
        self.answerer = answerer
        self.author = author

    def actionize(self):
        self.answerer.answer(self.actionizer.read_book(self.author))


class PlayAlbumIntention(Intention):
    actionizer: Actionizer
    answerer: Answerer
    artist: Optional[str]
    title: Optional[str]

    def __init__(self, actionizer: Actionizer, answerer: Answerer, artist: Optional[str], title: Optional[str]):
        super().__init__()
        self.actionizer = actionizer
        self.answerer = answerer
        self.artist = artist
        self.title = title

    def actionize(self):
        self.answerer.answer(self.actionizer.play_album(self.artist, self.title))
