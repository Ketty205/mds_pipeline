from concurrent.futures import ThreadPoolExecutor
import time
import logging
from src.models import Minibatch, FileBucket
from src.interfaces import MessageSource, FileSource, BucketStrategy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')

class DataPipelineProcessor:
    def __init__(self, worker_pool_size: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=worker_pool_size, thread_name_prefix="WorkerThread")

    def _process_minibatch_worker(self, minibatch: Minibatch):
        logging.info(f"Obrada minibatch-a sa {len(minibatch.messages)} poruka.")
        time.sleep(0.2)

    def _process_bucket_worker(self, bucket: FileBucket):
        logging.info(f"Obrada fajl bucket-a ukupne veličine {bucket.total_size_mb:.2f} MB sa {len(bucket.files)} fajlova.")
        time.sleep(0.2)

    def run_streaming_pipeline(self, source: MessageSource, window_duration_sec: float = 5.0):
        current_batch = Minibatch()
        window_end_time = None

        for msg in source.stream_messages():
            current_time = time.time()

            if window_end_time is None:
                window_end_time = current_time + window_duration_sec
                current_batch.messages.append(msg)
            elif current_time < window_end_time:
                current_batch.messages.append(msg)
            else:
                self.executor.submit(self._process_minibatch_worker, current_batch)
                current_batch = Minibatch(messages=[msg])
                window_end_time = current_time + window_duration_sec

        if current_batch.messages:
            self.executor.submit(self._process_minibatch_worker, current_batch)

    def run_batch_pipeline(self, file_source: FileSource, strategy: BucketStrategy, target_size_mb: float = 10.0):
        files = file_source.fetch_nightly_files()
        buckets = strategy.pack(files, target_size_mb)
        
        for bucket in buckets:
            self.executor.submit(self._process_bucket_worker, bucket)

    def shutdown(self):
        self.executor.shutdown(wait=True)