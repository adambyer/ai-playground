import logging
from .vector_db import VectorDB
from .ai_model import AIModel
from .deprecated.chat_agent import ChatAgent as ChatAgentDeprecated
from .chat_service import ChatService

logger = logging.getLogger(__name__)


class ChatHandler:
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
    def get_response_from_agent_deprecated(cls, prompt: str):
        response = ChatAgentDeprecated.generate_response(prompt)
        return response

    @classmethod
    async def get_response_from_agent(cls, prompt: str, language: str):
        response = await ChatService.generate_response(prompt, language)
        return response
