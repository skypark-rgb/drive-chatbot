from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    def upsert(self, chunks, embeddings):
        pass

    @abstractmethod
    def search(self, query_vector, limit=5):
        pass