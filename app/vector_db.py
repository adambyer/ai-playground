import logging
import uuid
from abc import ABC, abstractmethod
from chromadb import PersistentClient, ClientAPI, Collection

LOGGER = logging.getLogger(__name__)
CONTENT_KEY = "content"


class VectorDB(ABC):
    client: ClientAPI = PersistentClient(path="./chroma_db")
    collection_name = "chat_cache"
    collection: Collection = client.get_or_create_collection(collection_name)

    @classmethod
    @abstractmethod
    def get_collection_count(cls) -> None:
        return cls.collection.count()

    @classmethod
    @abstractmethod
    def reset_collection(cls) -> None:
        LOGGER.info(f"Deleting collection with {cls.collection.count()} items.")
        cls.client.delete_collection(cls.collection_name)
        cls.collection = cls.client.create_collection(cls.collection_name)
        LOGGER.info(f"New collection created with {cls.collection.count()} items.")

    @classmethod
    @abstractmethod
    async def store_document(cls, embedding: list[float], content: str) -> None:
        # This needs to be async because it's called in create_task.
        cls.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            metadatas=[{CONTENT_KEY: content}],
        )
        LOGGER.info(
            f"Document stored. Collection count is now  {cls.collection.count()}."
        )

    @classmethod
    @abstractmethod
    def get_relevant_documentst(cls, embedding: list[float]) -> list[str]:
        results = cls.collection.query(
            query_embeddings=[embedding],
            n_results=10,
        )

        relevant_documents = []

        # We only searched for one embedding, so we're getting back a list with one entry.
        # The entry is also a list - of distances for each document.
        for i, distance in enumerate(results["distances"][0]):
            print(
                "*** distance: ",
                distance,
                results["metadatas"][0][i][CONTENT_KEY].strip(),
            )
            if distance < 0.4:
                relevant_documents.append(
                    results["metadatas"][0][i][CONTENT_KEY].strip()
                )

        return relevant_documents
