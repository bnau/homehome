from abc import abstractmethod, ABC
from typing import List

from ner.model.metadata import Album


class MetadataRetriever(ABC):

    @abstractmethod
    def get_albums(self) -> List[Album]:
        pass
