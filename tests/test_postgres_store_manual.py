import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1] / "src")
)

from dataclasses import dataclass

from config import DATABASE_URL, QDRANT_COLLECTION
from vector_store.postgres_store import PostgresStore


@dataclass
class FakeChunk:
    file_id: str
    document_name: str
    chunk_index: int
    text: str


def main():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

    store = PostgresStore(DATABASE_URL)

    collection_name = QDRANT_COLLECTION
    vector_size = 3

    store.create_collection(
        collection_name=collection_name,
        vector_size=vector_size,
    )

    chunks = [
        FakeChunk(
            file_id="file_1",
            document_name="Benefits Guide",
            chunk_index=0,
            text="Employees receive health insurance and retirement benefits.",
        ),
        FakeChunk(
            file_id="file_2",
            document_name="Holiday Calendar",
            chunk_index=0,
            text="The office is closed on major holidays.",
        ),
        FakeChunk(
            file_id="file_3",
            document_name="Basketball Notes",
            chunk_index=0,
            text="LeBron James is a basketball player.",
        ),
    ]

    embeddings = [
        [1, 0, 0],
        [0.9, 0.1, 0],
        [0, 0, 1],
    ]

    store.upsert(
        collection_name=collection_name,
        chunks=chunks,
        embeddings=embeddings,
    )

    print("Point count:", store.point_count(collection_name))

    results = store.search(
        collection_name=collection_name,
        query_vector=[1, 0, 0],
        limit=2,
    )

    for result in results:
        print(result.payload, "score:", result.score)

    store.delete_file(
        collection_name=collection_name,
        file_id="file_1",
    )

    print("Point count after delete:", store.point_count(collection_name))


if __name__ == "__main__":
    main()