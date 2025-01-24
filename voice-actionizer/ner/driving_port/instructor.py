from abc import ABC, abstractmethod

from ner.driven_port.actionizer import Actionizer
from ner.driven_port.answerer import Answerer
from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.driven_port.store import Store
from ner.orchestrator.main import Orchestrator


class Instructor(ABC):
    @abstractmethod
    def instruct(self, command: str):
        pass


class DomainInstructor:
    actionizer: Actionizer
    answerer: Answerer
    orchestrator: Orchestrator

    def __init__(self, actionizer: Actionizer, answerer: Answerer, metadata_retriever: MetadataRetriever, store: Store):
        self.actionizer = actionizer
        self.answerer = answerer
        self.orchestrator = Orchestrator(metadata_retriever, store)

    def instruct(self, command: str):
        factory = self.orchestrator.invoke(command)
        factory.create_intention(self.actionizer, self.answerer).actionize()
