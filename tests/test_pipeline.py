import pytest
from unittest.mock import MagicMock
from src.models import FileMetadata, Message
from src.interfaces import MessageSource, FileSource
from src.strategies import GreedyBucketStrategy
from src.processor import DataPipelineProcessor

def test_greedy_bucket_strategy():
    strategy = GreedyBucketStrategy()
    files = [
        FileMetadata(name="f1.bin", size_mb=4.0),
        FileMetadata(name="f2.bin", size_mb=7.0),
    ]
    buckets = strategy.pack(files, target_size_mb=10.0)
    assert len(buckets) == 2

def test_nightly_file_source_mock():
    mock_file_source = MagicMock(spec=FileSource)
    mock_file_source.fetch_nightly_files.return_value = [
        FileMetadata(name="night_1.bin", size_mb=1.5)
    ]
    files = mock_file_source.fetch_nightly_files()
    assert len(files) == 1
    assert files[0].size_mb == 1.5