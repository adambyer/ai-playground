import asyncio
import logging
from .vector_db import VectorDB
from .ai_model import generate_embedding, prompt

logger = logging.getLogger(__name__)


async def get_response(text: str):
    logger.info(f"CHAT SERVICE: text: {text}")
    # Create embedding for incoming text
    embedding: list[float] = await generate_embedding(text)
    logger.info(f"CHAT SERVICE: embedding: {len(embedding)}")

    # Use incoming embedding to check for cached response
    response: str | None = VectorDB.get_document(embedding)

    if response:
        logger.info("CHAT SERVICE: cached response: {response}")
        yield response.encode()
        return

    # No cached response. Generate one from the model.
    response: str = ""

    async for chunk in prompt(text):
        response += chunk
        yield chunk

    logger.info("CHAT SERVICE: non-cached response: {response}")

    # Offload saving of the new embedding
    asyncio.create_task(VectorDB.store_document(embedding, response))
