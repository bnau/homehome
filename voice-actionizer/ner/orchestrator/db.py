from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="demo_collection",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="demo_collection",
    embedding=OllamaEmbeddings(
        model="mxbai-embed-large",
    ),
)


def get_db():
    return vector_store


def add_document(doc: str):
    vector_store.add_documents([
        Document(
            page_content=doc,
        ),
    ])
