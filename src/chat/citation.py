from dataclasses import dataclass


@dataclass
class Citation:
    document_name: str
    chunk_index: int