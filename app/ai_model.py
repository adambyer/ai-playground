import aiohttp
import logging
import os

logger = logging.getLogger(__name__)


class AIModel:
    api_root = f"http://{os.getenv('OLLAMA_ROOT')}:11434/api"
    chat_model = "mistral"
    embedding_model = "all-minilm"

    def __init__(self):
        raise TypeError("AiModel is a utility class and cannot be instantiated.")

    @classmethod
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
    async def generate_response(cls, prompt: str):
        cls.logger.info("AI MODEL prompt: {prompt}")
        uri = f"{cls.api_root}/generate"
        request_payload = {
            "model": cls.chat_model,
            "prompt": prompt,
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
