from embeddings.embedding_client import EmbeddingClient


class Retriever:

    def __init__(self, embedding_client, vector_store, collection_name):
        self.embedding_client = embedding_client
        self.vector_store = vector_store
        self.collection_name = collection_name

    def retrieve(self, question: str, limit=10):

        query_embedding = self.embedding_client.embed_text(question)

        return self.vector_store.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )