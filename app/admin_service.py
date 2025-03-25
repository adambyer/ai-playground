from .ai_model import AiModel
from .vector_db import VectorDB


class AdminService:
    def __init__(self):
        raise TypeError("AdminService is a utility class and cannot be instantiated.")

    @staticmethod
    async def add_document(content: str) -> None:
        embedding: list[float] = await AiModel.generate_embedding(content)
        await VectorDB.store_document(embedding, content)
