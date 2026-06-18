from dataclasses import dataclass


@dataclass
class DriveFile:
    id: str
    name: str
    mime_type: str