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

        parsed = 0
        skipped = 0
        failed = 0

        for file in files:

            logger.info(f"Processing: {file.name}")

            try:
                document = self.parser_registry.parse(file)

                if document is None:
                    skipped += 1
                    logger.warning(
                        f"Skipping unsupported file: {file.name}"
                    )
                    continue
                    
                documents.append(document)
                parsed += 1
            
            except Exception as e:
                failed += 1
                logger.error(
                    f"Failed to parse {file.name}: {e}"
                )



        logger.info("")

        logger.info("========== Synchronization Summary ==========")
        logger.info(f"Parsed:      {parsed}")
        logger.info(f"Skipped:    {skipped}")
        logger.info(f"Failed:      {failed}")
        logger.info(f"Documents:   {len(documents)}")
        logger.info("============================================")

        return documents