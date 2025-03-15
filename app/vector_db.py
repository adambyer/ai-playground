import logging
import uuid
from abc import ABC, abstractmethod
from chromadb import PersistentClient, ClientAPI, Collection

LOGGER = logging.getLogger(__name__)


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
            metadatas=[{"content": content}],
        )
        LOGGER.info(
            f"Document stored. Collection count is now  {cls.collection.count()}."
        )

    @classmethod
    @abstractmethod
    def get_document(cls, embedding: list[float]) -> str | None:
        results = cls.collection.query(
            query_embeddings=[embedding],
            n_results=1,
        )

        # We always get the closest match but it still might not be relevant so we check the distance.
        if not results["ids"][0] or results["distances"][0][0] > 0.05:
            return None

        return results["metadatas"][0][0]["content"].strip()
