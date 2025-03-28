import logging
from .vector_db import VectorDB
from .ai_model import AIModel
from .chat_agent import ChatAgent

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        raise TypeError("ChatService is a utility class and cannot be instantiated.")

    @classmethod
    async def get_response(cls, prompt: str):
        logger.info(f"ChatService: prompt: {prompt}")
        # Create embedding for incoming prompt
        embedding: list[float] = await AIModel.generate_embedding(prompt)

        # Use incoming embedding to check for relevant context documents
        relevant_documents: list[str] = VectorDB.get_relevant_documentst(embedding)
        logger.info(f"ChatService: relevant_documents: {relevant_documents}")

        prompt = f"Prompt: {prompt}\n\nResponse:"

        if relevant_documents:
            context = "\n".join(relevant_documents)
            prompt = f"Context: {context}\n\n{prompt}"

        cls.logger.info(f"ChatService: prompt: {prompt}")
        async for chunk in AIModel.generate_response(prompt):
            yield chunk

    @classmethod
    def get_response_langchain(cls, prompt: str):
        response = ChatAgent.generate_response(prompt)
        print("*** response: ", response)
        return response
