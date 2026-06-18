from parsers.parser_registry import ParserRegistry
from ingestion.ingestion_engine import IngestionEngine


from config import (
    APP_NAME,
    APP_VERSION,
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_DRIVE_FOLDER_ID,
)

from drive_service import client
from drive_service.client import DriveClient



def main():
    print(f"Welcome to {APP_NAME}")
    print(f"Version: {APP_VERSION}")
    print()


    client = DriveClient(GOOGLE_CREDENTIALS_PATH)

    registry = ParserRegistry(client)

    engine = IngestionEngine(
        drive_client=client,
        parser_registry=registry,
    )

    documents = engine.ingest_folder(
        GOOGLE_DRIVE_FOLDER_ID
    )

    for document in documents:
        print("=" * 60)
        print(document.name)
        print("-" * 60)
        print(document.text[:500])
        print()


if __name__ == "__main__":
    main()