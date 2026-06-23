from config import (
    OPENAI_API_KEY,
    QDRANT_PATH,
    QDRANT_COLLECTION,
)

from embeddings.embedding_client import EmbeddingClient
from vector_store.qdrant_store import QdrantStore
from retrieval.retriever import Retriever
from chat.chat_engine import ChatEngine


def create_chatbot():

    embedding_client = EmbeddingClient(
        OPENAI_API_KEY
    )

    store = QdrantStore(QDRANT_PATH)

    retriever = Retriever(
        embedding_client=embedding_client,
        vector_store=store,
        collection_name=QDRANT_COLLECTION,
    )

    return ChatEngine(
        retriever=retriever,
        embedding_client=embedding_client,
    )