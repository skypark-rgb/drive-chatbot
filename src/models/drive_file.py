from dataclasses import dataclass
from typing import Optional


@dataclass
class DriveFile:
    id: str
    name: str
    mime_type: str
    
    modified_time: Optional[str] = None
    created_time: Optional[str] = None
    md5_checksum: Optional[str] = None
    size: Optional[int] = None
