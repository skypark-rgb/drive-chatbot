from dataclasses import dataclass


@dataclass
class Document:
    id: str
    name: str
    mime_type: str
    text: str