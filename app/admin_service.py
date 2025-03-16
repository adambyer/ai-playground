from abc import ABC, abstractmethod

from .ai_model import AiModel
from .vector_db import VectorDB


class AdminService(ABC):
    @staticmethod
    @abstractmethod
    async def add_document(content: str) -> None:
        embedding: list[float] = await AiModel.generate_embedding(content)
        await VectorDB.store_document(embedding, content)
