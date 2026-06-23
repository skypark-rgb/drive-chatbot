from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from vector_store.vector_store import VectorStore
import hashlib



class QdrantStore(VectorStore):

    def __init__(self, path: str):
        self.client = QdrantClient(path=path)

    def create_collection(self, collection_name: str, vector_size: int):

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if collection_name in existing:
            print("✔ Using existing Qdrant collection")
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        print("✔ Created Qdrant collection")


    def upsert(self, collection_name: str, chunks, embeddings):

        points = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

            points.append(
                PointStruct(
                    id=int(
                        hashlib.md5(
                            f"{chunk.file_id}_{chunk.chunk_index}".encode()
                        ).hexdigest()[:16],
                        16,
                    ),
                    
                    vector=embedding,
                    payload={
                        "file_id": chunk.file_id,
                        "document_name": chunk.document_name,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                    },
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points,
        )
    
    def delete_file(self, collection_name: str, file_id: str):

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if collection_name not in existing:
            return

        self.client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="file_id",
                        match=MatchValue(value=file_id),
                    )
                ]
            ),
        )


    def search(self, collection_name: str, query_vector, limit: int = 5):

        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
        )

        return results.points

    def point_count(self, collection_name: str):

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if collection_name not in existing:
            return 0

        return self.client.count(
            collection_name=collection_name
        ).count