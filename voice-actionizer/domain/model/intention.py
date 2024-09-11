from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional


class IntentionFactory(BaseModel):
    action: Optional[str] = Field(title="Action", description="Action to perform",default="")
    author: Optional[str] = Field(title="Author", description="Author of the book",default="")
    title: Optional[str] = Field(title="Title", description="Title of the album",default="")

    def create_intention(self, actionizer: Actionizer, answerer: Answerer):
        if self.action == "readBook":
            return ReadIntention(actionizer, answerer, self.author)
        else:
            raise Exception("Unknown action")


class Intention(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def actionize(self):
        pass


class ReadIntention(Intention):
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
