import uuid
from chromadb import PersistentClient, ClientAPI, Collection

client: ClientAPI = PersistentClient(path="./chroma_db")
collection: Collection = client.get_or_create_collection("chat_cache")


async def save_embedding(embedding: str, response: str) -> None:
    # This needs to be async because it's called in create_task.
    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embedding],
        metadatas=[{"response": response}],
    )


def get_by_embedding(embedding: str) -> str | None:
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
    )

    # We always get the closest match but it still might not be relevant so we check the distance.
    if not results["ids"][0] or results["distances"][0][0] > 0.05:
        return None

    return results["metadatas"][0][0]["response"].strip()
