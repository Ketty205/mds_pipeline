from abc import ABC, abstractmethod
from typing import List, Generator
from src.models import Message, FileMetadata, FileBucket

class MessageSource(ABC):
    @abstractmethod
    def stream_messages(self) -> Generator[Message, None, None]:
        pass

class FileSource(ABC):
    @abstractmethod
    def fetch_nightly_files(self) -> List[FileMetadata]:
        pass

class BucketStrategy(ABC):
    @abstractmethod
    def pack(self, files: List[FileMetadata], target_size_mb: float) -> List[FileBucket]:
        pass