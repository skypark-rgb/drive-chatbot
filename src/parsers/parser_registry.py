from parsers.google_docs_parser import GoogleDocsParser
from parsers.pdf_parser import PDFParser


class ParserRegistry:
    def __init__(self, drive_client):
        self.parsers = {
            "application/vnd.google-apps.document": GoogleDocsParser(drive_client),
            "application/pdf": PDFParser(drive_client),
        }
        

    def parse(self, file_metadata):
        mime_type = file_metadata.mime_type

        parser = self.parsers.get(mime_type)

        if parser is None:
            return None

        return parser.parse(file_metadata)