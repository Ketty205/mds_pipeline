from typing import List
from src.interfaces import BucketStrategy
from src.models import FileMetadata, FileBucket

class GreedyBucketStrategy(BucketStrategy):
    def pack(self, files: List[FileMetadata], target_size_mb: float) -> List[FileBucket]:
        buckets: List[FileBucket] = []
        current_bucket = FileBucket()

        for file in files:
            if current_bucket.total_size_mb + file.size_mb > target_size_mb and current_bucket.files:
                buckets.append(current_bucket)
                current_bucket = FileBucket()
            
            current_bucket.files.append(file)
            current_bucket.total_size_mb += file.size_mb

        if current_bucket.files:
            buckets.append(current_bucket)

        return buckets