from dataclasses import dataclass

@dataclass
class TextChunk:
    document_id: str
    chunk_index: int
    text: str