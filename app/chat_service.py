import logging
from .vector_db import VectorDB
from .ai_model import generate_embedding, generate_response

logger = logging.getLogger(__name__)


async def get_response(text: str):
    logger.info(f"CHAT SERVICE: text: {text}")
    # Create embedding for incoming text
    embedding: list[float] = await generate_embedding(text)

    # Use incoming embedding to check for relevant context documents
    relevant_documents: list[str] = VectorDB.get_relevant_documentst(embedding)
    logger.info(f"CHAT SERVICE: relevant_documents: {relevant_documents}")

    prompt = f"Prompt: {text}\n\nResponse:"

    if relevant_documents:
        context = "\n".join(relevant_documents)
        prompt = f"Context: {context}\n\n{prompt}"

    logger.info(f"CHAT SERVICE: prompt: {prompt}")
    async for chunk in generate_response(prompt):
        yield chunk
