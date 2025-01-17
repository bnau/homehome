from abc import ABC, abstractmethod

from ner.driven_port.actionizer import Actionizer
from ner.driven_port.answerer import Answerer
from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.orchestrator.graph import invoke_graph


class Instructor(ABC):
    @abstractmethod
    def instruct(self, command: str):
        pass


class DomainInstructor:
    actionizer: Actionizer
    answerer: Answerer
    metadata_retriever: MetadataRetriever

    def __init__(self, actionizer: Actionizer, answerer: Answerer, metadata_retriever: MetadataRetriever):
        self.actionizer = actionizer
        self.answerer = answerer
        self.metadata_retriever = metadata_retriever

    def instruct(self, command: str):
        factory = invoke_graph(command, self.metadata_retriever)
        factory.create_intention(self.actionizer, self.answerer).actionize()
