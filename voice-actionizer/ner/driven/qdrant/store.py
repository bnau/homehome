from typing import List

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from ner.driven_port.store import Store


class QdrantStore(Store):

    def __init__(self, location: str) -> None:
        client = QdrantClient(location)

        client.create_collection(
            collection_name="demo_collection",
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

        self.__store = QdrantVectorStore(
            client=client,
            collection_name="demo_collection",
            embedding=OllamaEmbeddings(
                model="mxbai-embed-large",
            ),
        )

    def add(self, doc: str) -> None:
        self.__store.add_documents([
            Document(
                page_content=doc,
            ),
        ])

    def retrieve(self, query: str) -> List[str]:
        return [doc.page_content for doc in self.__store.similarity_search(query)]
