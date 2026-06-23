from io import BytesIO

from pypdf import PdfReader

from models.document import Document


class PDFParser:
    def __init__(self, drive_client):
        self.drive_client = drive_client

    def parse(self, file_metadata):
        pdf_bytes = self.drive_client.download_file(
            file_metadata.id
        )

        reader = PdfReader(BytesIO(pdf_bytes))

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return Document(
            file_id=file_metadata.id,
            name=file_metadata.name,
            mime_type=file_metadata.mime_type,
            text=text,
        )