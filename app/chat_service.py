import logging
from .vector_db import VectorDB
from .ai_model import AiModel


class ChatService:
    logger = logging.getLogger(__name__)

    def __init__(self):
        raise TypeError("ChatService is a utility class and cannot be instantiated.")

    @classmethod
    async def get_response(cls, text: str):
        cls.logger.info(f"CHAT SERVICE: text: {text}")
        # Create embedding for incoming text
        embedding: list[float] = await AiModel.generate_embedding(text)

        # Use incoming embedding to check for relevant context documents
        relevant_documents: list[str] = VectorDB.get_relevant_documentst(embedding)
        cls.logger.info(f"CHAT SERVICE: relevant_documents: {relevant_documents}")

        prompt = f"Prompt: {text}\n\nResponse:"

        if relevant_documents:
            context = "\n".join(relevant_documents)
            prompt = f"Context: {context}\n\n{prompt}"

        cls.logger.info(f"CHAT SERVICE: prompt: {prompt}")
        async for chunk in AiModel.generate_response(prompt):
            yield chunk
