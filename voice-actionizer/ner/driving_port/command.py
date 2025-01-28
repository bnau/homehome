from abc import ABC, abstractmethod

from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.driven_port.store import Store
from ner.orchestrator.main import Orchestrator


class Command(ABC):
    @abstractmethod
    def launch(self, command: str):
        pass


class DomainCommand:
    orchestrator: Orchestrator

    def __init__(self, metadata_retriever: MetadataRetriever, store: Store):
        self.orchestrator = Orchestrator(metadata_retriever, store)

    def launch(self, command: str):
        if command == "store_albums":
            self.orchestrator.store_albums()
        else:
            RuntimeError(f"Unknown command {command}")

