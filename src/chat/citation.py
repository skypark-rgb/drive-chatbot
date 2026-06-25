from dataclasses import dataclass


@dataclass
class Citation:
    file_id: str
    document_name: str
    chunk_index: int
    text: str

    @property
    def url(self) -> str:
        return f"https://drive.google.com/file/d/{self.file_id}/view"