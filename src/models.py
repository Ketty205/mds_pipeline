from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Message:
    id: str
    timestamp: float
    payload: Any

@dataclass
class FileMetadata:
    name: str
    size_mb: float

@dataclass
class Minibatch:
    messages: List[Message] = field(default_factory=list)

@dataclass
class FileBucket:
    files: List[FileMetadata] = field(default_factory=list)
    total_size_mb: float = 0.0