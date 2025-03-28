import logging
import os
from langchain_ollama import OllamaLLM
from langchain.chains.retrieval_qa.base import RetrievalQA

from .vector_db_langchain import VectorDBLangChain

print("*** os.getenv('OLLAMA_ROOT')", os.getenv("OLLAMA_ROOT"))


class AIModelLangChain:
    logger = logging.getLogger(__name__)
    chat_model = OllamaLLM(
        model="mistral",
        base_url=f"http://{os.getenv('OLLAMA_ROOT')}:11434",
    )
    retriever = VectorDBLangChain.store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=chat_model,
        retriever=retriever,
        return_source_documents=True,
    )

    @classmethod
    def generate_response(cls, prompt: str) -> str:
        docs_with_scores = VectorDBLangChain.store.similarity_search_with_score(
            prompt,
            k=4,
        )

        # These scores are not very accurate, possibly because ChromaDB is expecting normalized embeddings,
        # but the Hugging Face (and many other) embedding models output raw vectors.
        # Options are to either stick to model/db pairs that match, or manually normalize, but I'm not going
        # to worry about it for now for this playground.
        cls.logger.info(f"AI Model LangChain docs_with_scores: {docs_with_scores}")
        docs = [doc for doc, score in docs_with_scores if score < 1.5]

        if docs:
            response = cls.qa_chain.invoke({"query": prompt})
            output = response["result"]
        else:
            response = cls.chat_model.invoke(prompt)
            output = f"None of the provided documents are relevant to your prompt. Here's some general information that may be useful: {response}"

        cls.logger.info(f"AI Model LangChain response: {response}")
        return output.strip()
