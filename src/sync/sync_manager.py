import sqlite3
from pathlib import Path



class SyncManager:

    def __init__(self, db_path="data/sync.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS synced_files (
                file_id TEXT PRIMARY KEY,
                modified_time TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def is_modified(self, drive_file):
        self.cursor.execute(
            """
            SELECT modified_time
            FROM synced_files
            WHERE file_id = ?
            """,
            (drive_file.id,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return True

        return row[0] != drive_file.modified_time

    def mark_synced(self, drive_file):


        self.cursor.execute(
            """
            INSERT OR REPLACE INTO synced_files
            (file_id, modified_time)
            VALUES (?, ?)
            """,
            (
                drive_file.id,
                drive_file.modified_time,
            ),
        )

        self.connection.commit()


    def remove_file(self, file_id):
        self.cursor.execute(
            """
            DELETE FROM synced_files
            WHERE file_id = ?
            """,
            (file_id,),
        )

        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_all_file_ids(self):

        self.cursor.execute(
            """
            SELECT file_id
            FROM synced_files
            """
        )

        return {
            row[0]
            for row in self.cursor.fetchall()
        }