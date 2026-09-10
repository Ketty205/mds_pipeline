# Concurrent Data Processing Pipeline

Arhitektura sistema za paralelno procesiranje real-time stream poruka (poissonova raspodela) i batch obradu noćnih fajlova (strategija pakovanja u bucket-e), realizovana kroz OOP i SOLID principe u Python-u.

## Arhitektura i SOLID Principi
- **Single Responsibility:** Svaka klasa (izvor, strategija, procesor) ima jasnu i izdvojenu ulogu.
- **Open/Closed & Strategy Pattern:** Dodavanje nove strategije pakovanja fajlova ili promene izvora poruka (npr. prelazak sa generatora na Kafku) ne zahteva izmenu postojeće procesne logike, već samo implementaciju definisanih ABC interfejsa.
- **Dependency Inversion:** `DataPipelineProcessor` zavisi od apstrakcija (`MessageSource`, `FileSource`, `BucketStrategy`), a ne od konkretnih implementacija.

## Pokretanje testova
```bash
pytest -v