from src.sources import PoissonMessageSource, NightlyFileSource
from src.strategies import GreedyBucketStrategy
from src.processor import DataPipelineProcessor

if __name__ == "__main__":
    print("--- Pokretanje Data Pipeline Sistema ---")

    # Inicijalizacija procesora sa 10 radnih niti
    processor = DataPipelineProcessor(worker_pool_size=10)

    # 1. Testiranje streaming toka (Poisson raspodela poruka)
    print("\n[STREAMING] Pokretanje obrade poruka...")
    stream_source = PoissonMessageSource(rate_per_min=10.0, total_messages=15)
    processor.run_streaming_pipeline(stream_source, window_duration_sec=2.0)

    # 2. Testiranje noćnog batch toka (Pakovanje fajlova)
    print("\n[BATCH] Pokretanje noćne obrade fajlova...")
    file_source = NightlyFileSource(count=30, scale_size=2.0)
    strategy = GreedyBucketStrategy()
    processor.run_batch_pipeline(file_source, strategy, target_size_mb=10.0)

    # Zatvaranje executor-a
    processor.shutdown()
    print("\n--- Sistem uspešno završio sa radom ---")