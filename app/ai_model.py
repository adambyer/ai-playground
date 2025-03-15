import aiohttp
import logging

logger = logging.getLogger(__name__)

API_ROOT = "http://localhost:11434/api"
CHAT_MODEL = "mistral"
EMBEDDING_MODEL = "all-minilm"


async def generate_embedding(text: str) -> list[float]:
    logger.info(f"AI MODEL generate_embedding: text: {text}")
    uri = f"{API_ROOT}/embed"
    request_payload = {
        "model": EMBEDDING_MODEL,
        "input": text,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(uri, json=request_payload) as response:
            response_payload = await response.json()

    return response_payload["embeddings"][0]


async def prompt(text: str):
    logger.info("AI MODEL prompt: text: {text}")
    uri = f"{API_ROOT}/generate"
    request_payload = {
        "model": CHAT_MODEL,
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
