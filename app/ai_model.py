from abc import ABC, abstractmethod
import aiohttp
import logging


class AiModel(ABC):
    logger = logging.getLogger(__name__)
    api_root = "http://localhost:11434/api"
    chat_model = "mistral"
    embedding_model = "all-minilm"

    @classmethod
    @abstractmethod
    async def generate_embedding(cls, text: str) -> list[float]:
        cls.logger.info(f"AI MODEL generate_embedding: text: {text}")
        uri = f"{cls.api_root}/embed"
        request_payload = {
            "model": cls.embedding_model,
            "input": text,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(uri, json=request_payload) as response:
                response_payload = await response.json()

        return response_payload["embeddings"][0]

    @classmethod
    @abstractmethod
    async def generate_response(cls, text: str):
        cls.logger.info("AI MODEL prompt: text: {text}")
        uri = f"{cls.api_root}/generate"
        request_payload = {
            "model": cls.chat_model,
            "prompt": text,
            "stream": True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(uri, json=request_payload) as response:
                # response_payload = await response.json()

                # Stream chunks as received.
                # Note that this model seems to stream in large chunks,
                # so if the full response is pretty short, you might get it all at once.
                async for chunk in response.content.iter_any():
                    yield chunk.decode()
