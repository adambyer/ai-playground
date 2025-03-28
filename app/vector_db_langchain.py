import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# This class demonstrates usage of ChromaDB via Langchain.
# For working with the ChromaDB library, see vector_db.py.

logger = logging.getLogger(__name__)


class VectorDBLangChain:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    store = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./chroma_db_langchain",
    )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    @classmethod
    def add_document_from_file(cls, file_path: str):
        logger.info("VectorDBLangChain: Add Document from File")
        loader = TextLoader(file_path)

        # In this case, load will return a list with one entry (it's a list because other loaders may return more than one document).
        incoming_docs = loader.load()

        # Split the incoming documents (really just one) into the desired sized chunks.
        docs = cls.splitter.split_documents(incoming_docs)

        cls.store.add_documents(docs)
