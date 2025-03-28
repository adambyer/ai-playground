import logging
import uuid
from chromadb import PersistentClient, ClientAPI, Collection

logger = logging.getLogger(__name__)
CONTENT_KEY = "content"

# This class demonstrates usage of ChromaDB via it's library.
# For working with ChromaDB via Langchain, see vector_store.py.


class VectorDB:
    client: ClientAPI = PersistentClient(path="./chroma_db")
    collection_name = "chat_cache"
    collection: Collection = client.get_or_create_collection(collection_name)

    def __init__(self):
        raise TypeError("VectorDB is a utility class and cannot be instantiated.")

    @classmethod
    def get_collection_count(cls) -> None:
        return cls.collection.count()

    @classmethod
    def reset_collection(cls) -> None:
        logger.info(f"Deleting collection with {cls.collection.count()} items.")
        cls.client.delete_collection(cls.collection_name)
        cls.collection = cls.client.create_collection(cls.collection_name)
        logger.info(f"New collection created with {cls.collection.count()} items.")

    @classmethod
    def store_document(cls, embedding: list[float], content: str) -> None:
        cls.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            metadatas=[{CONTENT_KEY: content}],
        )
        logger.info(
            f"Document stored. Collection count is now  {cls.collection.count()}."
        )

    @classmethod
    def get_relevant_documentst(cls, embedding: list[float]) -> list[str]:
        results = cls.collection.query(
            query_embeddings=[embedding],
            n_results=10,
        )

        relevant_documents = []

        # We only searched for one embedding, so we're getting back a list with one entry.
        # The entry is also a list - of distances for each document.
        for i, distance in enumerate(results["distances"][0]):
            if distance < 1.0:
                relevant_documents.append(
                    results["metadatas"][0][i][CONTENT_KEY].strip()
                )

        return relevant_documents
