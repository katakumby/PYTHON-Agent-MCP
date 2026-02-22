import os
import sys
import logging
import json  # <--- Dodano do pretty-printingu JSONa
from dotenv import load_dotenv

# Upewnij się, że ten import pasuje do struktury Twojego projektu
from buissnes_agent.QdrantDatabaseStore import QdrantDatabaseStore

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("DB-Viewer")

# Ładowanie zmiennych środowiskowych
load_dotenv()


def view_entries(limit: int = 5):
    """
    Pobiera i wyświetla N ostatnich wpisów z kolekcji Qdrant.
    Wyświetla PEŁNY PAYLOAD (wszystkie metadane) w formacie JSON.
    """

    # 1. Pobieranie konfiguracji z .env
    qdrant_url = os.getenv("QDRANT_API")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("COLLECTION_NAME", "knowledgebase")

    if not qdrant_url:
        logger.error("Brak QDRANT_API w pliku .env")
        return

    # 2. Inicjalizacja Twojej klasy Store
    try:
        store = QdrantDatabaseStore(
            url=qdrant_url,
            api_key=qdrant_key,
            collection_name=collection_name,
            vector_size=1536
        )
    except Exception as e:
        logger.error(f"Nie udało się połączyć z Qdrant: {e}")
        return

    print(f"\n--- PRZEGLĄDANIE KOLEKCJI: {collection_name} ---")
    try:
        count = store.count()
        print(f"Ilość dokumentów w bazie: {count}")
    except Exception:
        print("Nie udało się pobrać licznika dokumentów.")

    print(f"Pobieranie {limit} wpisów...\n")

    try:
        # 3. Użycie metody SCROLL z klienta Qdrant
        records, next_page_offset = store.client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )

        if not records:
            print("Brak wpisów w bazie.")
            return

        # 4. Wyświetlanie wyników
        for i, record in enumerate(records, 1):
            payload = record.payload

            print(f"[{i}] Qdrant UUID: {record.id}")
            print("    PEŁNE DANE (PAYLOAD):")

            # json.dumps sformatuje słownik payloadu w czytelną strukturę
            # ensure_ascii=False pozwala wyświetlać polskie znaki
            print(json.dumps(payload, indent=4, ensure_ascii=False))

            print("-" * 80)

    except Exception as e:
        logger.error(f"Błąd podczas pobierania danych: {e}")


if __name__ == "__main__":
    # Obsługa argumentu z linii poleceń
    qty = 5
    if len(sys.argv) > 1:
        try:
            qty = int(sys.argv[1])
        except ValueError:
            print("Podaj poprawną liczbę całkowitą.")
            sys.exit(1)

    view_entries(qty)