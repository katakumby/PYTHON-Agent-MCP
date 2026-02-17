import os
import sys
import logging
from dotenv import load_dotenv

from buissnes_agent.QdrantDatabaseStore import QdrantDatabaseStore

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("DB-Viewer")

# Ładowanie zmiennych środowiskowych
load_dotenv()


def view_entries(limit: int = 5):
    """
    Pobiera i wyświetla N ostatnich wpisów z kolekcji Qdrant.
    """

    # 1. Pobieranie konfiguracji z .env
    qdrant_url = os.getenv("QDRANT_API")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("COLLECTION_NAME")

    # 2. Inicjalizacja Twojej klasy Store
    # Vector size nie ma znaczenia przy odczycie, dajemy 1536 domyślnie
    store = QdrantDatabaseStore(
        url=qdrant_url,
        api_key=qdrant_key,
        collection_name=collection_name,
        vector_size=1536
    )

    print(f"\n--- PRZEGLĄDANIE KOLEKCJI: {collection_name} ---")
    print(f"Ilość dokumentów w bazie: {store.count()}")
    print(f"Pobieranie {limit} wpisów...\n")

    try:
        # 3. Użycie metody SCROLL z klienta Qdrant (omijamy metody klasy wrapper)
        # with_vectors=False -> nie pobieramy wektorów (liczb), żeby nie śmiecić w konsoli
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

            # Wyciągamy kluczowe informacje
            text_preview = payload.get('text', 'BRAK TREŚCI')[:200] + "..."  # Skracamy tekst
            source_file = payload.get('source_file', 'Nieznane źródło')
            doc_type = payload.get('type', 'N/A')

            print(f"[{i}] ID: {record.id}")
            print(f"Źródło: {source_file}")
            print(f"Typ: {doc_type}")
            print(f"Treść (fragment): {text_preview}")
            print("-" * 60)

    except Exception as e:
        logger.error(f"Błąd podczas pobierania danych: {e}")


if __name__ == "__main__":
    # Obsługa argumentu z linii poleceń (np. python test_script_view_entries.py 10)
    qty = 2000
    if len(sys.argv) > 1:
        try:
            qty = int(sys.argv[1])
        except ValueError:
            print("Podaj poprawną liczbę całkowitą.")
            sys.exit(1)

    view_entries(qty)