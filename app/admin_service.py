import logging
import os
from .ai_model import AIModel
from .vector_db import VectorDB
from .vector_db_langchain import VectorDBLangChain

logger = logging.getLogger(__name__)
UPLOAD_PATH = "uploads"
os.makedirs(UPLOAD_PATH, exist_ok=True)


class AdminService:
    def __init__(self):
        raise TypeError("AdminService is a utility class and cannot be instantiated.")

    @staticmethod
    async def add_document(content: str) -> None:
        logger.info("AdminService: Add Document")
        embedding: list[float] = await AIModel.generate_embedding(content)
        await VectorDB.store_document(embedding, content)

    @staticmethod
    async def add_document_from_bytes(content: bytes, filename: str) -> None:
        logger.info("AdminService: Add Document from Bytes")
        file_path = os.path.join(UPLOAD_PATH, filename)

        with open(file_path, "wb") as f:
            f.write(content)

        VectorDBLangChain.add_document_from_file(file_path)

        os.remove(file_path)
