from dataclasses import dataclass


@dataclass
class Document:
    file_id: str
    name: str
    mime_type: str
    text: str