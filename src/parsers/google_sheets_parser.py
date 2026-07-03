import csv
from io import StringIO

from models.document import Document


class GoogleSheetsParser:
    def __init__(self, drive_client):
        self.drive_client = drive_client

    def parse(self, file_metadata):
        csv_text = self.drive_client.export_google_sheet_as_csv(
            file_metadata.id
        )

        reader = csv.reader(StringIO(csv_text))

        rows = list(reader)

        text_lines = []

        for row_index, row in enumerate(rows, start=1):
            cleaned_cells = [
                cell.strip()
                for cell in row
                if cell.strip()
            ]

            if not cleaned_cells:
                continue

            text_lines.append(
                f"Row {row_index}: " + " | ".join(cleaned_cells)
            )

        return Document(
            file_id=file_metadata.id,
            name=file_metadata.name,
            mime_type=file_metadata.mime_type,
            text="\n".join(text_lines),
        )