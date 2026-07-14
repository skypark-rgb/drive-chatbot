from config import (
    OPENAI_API_KEY,
    QDRANT_PATH,
    QDRANT_COLLECTION,
    DATABASE_URL,
    VECTOR_STORE,
)

from vector_store.postgres_store import PostgresStore

from embeddings.embedding_client import EmbeddingClient
from vector_store.qdrant_store import QdrantStore
from retrieval.retriever import Retriever
from chat.chat_engine import ChatEngine


def create_chatbot():

    embedding_client = EmbeddingClient(
        OPENAI_API_KEY
    )

    if VECTOR_STORE == "postgres":
        print("✓ Using Postgres vector store")
        store = PostgresStore(DATABASE_URL)

    else:
        print("✓ Using Qdrant vector store")
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