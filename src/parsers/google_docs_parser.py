
from models.document import Document


class GoogleDocsParser:
    def __init__(self, drive_client):
        self.drive_client = drive_client

    def parse(self, file_metadata):
        text = self.drive_client.export_google_doc_as_text(
            file_metadata.id
        )

        return Document(
            id=file_metadata.id,
            name=file_metadata.name,
            mime_type=file_metadata.mime_type,
            text=text,
        )