import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

from vector_store.vector_store import VectorStore


class PostgresPoint:
    def __init__(self, payload: dict, score: float = None):
        self.payload = payload
        self.score = score


class PostgresStore(VectorStore):

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection = psycopg2.connect(database_url)

    def create_collection(self, collection_name: str, vector_size: int):
        table_name = self._table_name(collection_name)

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

                cursor.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id text PRIMARY KEY,
                        file_id text NOT NULL,
                        document_name text NOT NULL,
                        chunk_index integer NOT NULL,
                        text text NOT NULL,
                        embedding vector({vector_size}) NOT NULL
                    )
                    """
                )

                cursor.execute(
                    f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_embedding_idx
                    ON {table_name}
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                    """
                )

                cursor.execute(
                    f"""
                    CREATE INDEX IF NOT EXISTS {table_name}_file_id_idx
                    ON {table_name} (file_id)
                    """
                )

        print("✓ Postgres collection ready")

    def upsert(self, collection_name: str, chunks, embeddings):
        table_name = self._table_name(collection_name)

        rows = []

        for chunk, embedding in zip(chunks, embeddings):
            point_id = f"{chunk.file_id}_{chunk.chunk_index}"

            rows.append(
                (
                    point_id,
                    chunk.file_id,
                    chunk.document_name,
                    chunk.chunk_index,
                    chunk.text,
                    self._format_vector(embedding),
                )
            )

        with self.connection:
            with self.connection.cursor() as cursor:
                execute_values(
                    cursor,
                    f"""
                    INSERT INTO {table_name}
                        (id, file_id, document_name, chunk_index, text, embedding)
                    VALUES %s
                    ON CONFLICT (id)
                    DO UPDATE SET
                        file_id = EXCLUDED.file_id,
                        document_name = EXCLUDED.document_name,
                        chunk_index = EXCLUDED.chunk_index,
                        text = EXCLUDED.text,
                        embedding = EXCLUDED.embedding
                    """,
                    rows,
                )

    def search(self, collection_name: str, query_vector, limit: int = 5):
        table_name = self._table_name(collection_name)

        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"""
                SELECT
                    file_id,
                    document_name,
                    chunk_index,
                    text,
                    embedding <=> %s AS distance
                FROM {table_name}
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    self._format_vector(query_vector),
                    self._format_vector(query_vector),
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            PostgresPoint(
                payload={
                    "file_id": row["file_id"],
                    "document_name": row["document_name"],
                    "chunk_index": row["chunk_index"],
                    "text": row["text"],
                },
                score=row["distance"],
            )
            for row in rows
        ]

    def delete_file(self, collection_name: str, file_id: str):
        table_name = self._table_name(collection_name)

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    DELETE FROM {table_name}
                    WHERE file_id = %s
                    """,
                    (file_id,),
                )

    def point_count(self, collection_name: str):
        table_name = self._table_name(collection_name)

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = %s
                )
                """,
                (table_name,),
            )

            exists = cursor.fetchone()[0]

            if not exists:
                return 0

            cursor.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            )

            return cursor.fetchone()[0]

    def _format_vector(self, vector):
        return "[" + ",".join(str(value) for value in vector) + "]"

    def _table_name(self, collection_name: str):
        safe_name = collection_name.lower().replace("-", "_")
        return f"vector_{safe_name}"