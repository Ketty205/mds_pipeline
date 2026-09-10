import time
import random
from typing import Generator, List
from src.interfaces import MessageSource, FileSource
from src.models import Message, FileMetadata

class PoissonMessageSource(MessageSource):
    def __init__(self, rate_per_min: float = 10.0, total_messages: int = 50):
        self.rate_per_min = rate_per_min
        self.total_messages = total_messages

    def stream_messages(self) -> Generator[Message, None, None]:
        for i in range(self.total_messages):
            mean_interval = 60.0 / self.rate_per_min
            sleep_time = random.expovariate(1.0 / mean_interval)
            time.sleep(min(sleep_time, 0.05)) # Skraćeno radi testa
            yield Message(id=f"msg_{i}", timestamp=time.time(), payload=f"data_{i}")

class NightlyFileSource(FileSource):
    def __init__(self, count: int = 100, scale_size: float = 2.0):
        self.count = count
        self.scale_size = scale_size

    def fetch_nightly_files(self) -> List[FileMetadata]:
        files = []
        for i in range(self.count):
            size = random.expovariate(1.0 / self.scale_size)
            files.append(FileMetadata(name=f"file_{i}.bin", size_mb=round(size, 2)))
        return files