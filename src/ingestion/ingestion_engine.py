from logging_utils.logger import get_logger


logger = get_logger(__name__)


class IngestionEngine:
    def __init__(self, drive_client, parser_registry):
        self.drive_client = drive_client
        self.parser_registry = parser_registry

    def ingest_folder(self, folder_id):
        logger.info("Reading files from Google Drive...")

        files = self.drive_client.list_files(folder_id)

        documents = []

        for file in files:

            logger.info(f"Processing: {file.name}")

            document = self.parser_registry.parse(file)

            if document is None:
                logger.warning(
                    f"Skipping unsupported file: {file.name}"
                )
                continue

            documents.append(document)

        logger.info(f"Finished. Parsed {len(documents)} documents.")

        return documents