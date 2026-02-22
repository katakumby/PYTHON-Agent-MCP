import logging
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Distance

logger = logging.getLogger(__name__)


class QdrantDatabaseStore:
    def __init__(self, url: str, api_key: str, collection_name: str, vector_size: int = 1536):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(url=url, api_key=api_key)
        self._ensure_collection()

    def _ensure_collection(self):
        """Tworzy kolekcję tylko jeśli nie istnieje."""
        try:
            if not self.client.collection_exists(self.collection_name):
                logger.info(f"Tworzenie kolekcji: {self.collection_name} (dim: {self.vector_size})")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
                )
            else:
                logger.info(f"Kolekcja {self.collection_name} już istnieje.")
        except Exception as e:
            logger.error(f"Błąd inicjalizacji Qdrant: {e}")
            raise

    def count(self) -> int:
        """Zwraca liczbę wektorów w kolekcji."""
        try:
            return self.client.count(collection_name=self.collection_name).count
        except Exception:
            return 0

    def insert_batch(self, items: List[Dict[str, Any]]):
        """
        Wstawia paczkę dokumentów do Qdrant.
        Obsługuje konwersję ID (Hash -> UUID) oraz mapowanie Phrase.
        """
        if not items:
            return

        points = []

        for item in items:
            metadata = item["metadata"]
            raw_id = metadata.get("phrase_metadata_id")

            # 1. Walidacja i formatowanie ID (Qdrant wymaga UUID z myślnikami lub int)
            point_id = str(uuid.uuid4())  # Fallback
            if raw_id:
                try:
                    # Jeśli ID to 32-znakowy hash MD5, zamieniamy go na format UUID (8-4-4-4-12)
                    point_id = str(uuid.UUID(hex=raw_id))
                except ValueError:
                    # Jeśli to nie hex, zostawiamy jak jest (o ile to string) lub generujemy nowy
                    logger.warning(f"Nieprawidłowy format ID '{raw_id}', generuję nowy UUID.")
                    pass

            # 2. Przygotowanie Payloadu (Płaska struktura)
            payload = metadata.copy()

            # Gwarancja istnienia klucza 'phrase' (treść)
            if "phrase" not in payload:
                payload["phrase"] = item.get("text", "")

            # 3. Tworzenie punktu
            points.append(PointStruct(
                id=point_id,
                vector=item["vector"],
                payload=payload
            ))

        try:
            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info(f"Zapisano {len(points)} wektorów. Przykładowy ID: {points[0].id}")
        except Exception as e:
            logger.error(f"Błąd zapisu do Qdrant: {e}")

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Wyszukuje podobne wektory i zwraca zmapowane wyniki.
        Zaktualizowano do obsługi nowego schematu ('phrase' i 'metadata').
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )

            output = []
            for p in results:
                payload = p.payload or {}

                # Pobieramy treść (phrase ma priorytet nad text)
                content = payload.get("phrase") or payload.get("text") or ""

                # Zwracamy spójną strukturę
                output.append({
                    "text": content,  # Dla kompatybilności wstecznej
                    "metadata": payload,  # Pełne metadane (source, title, etc.)
                    "score": p.score
                })

            return output

        except Exception as e:
            logger.error(f"Błąd wyszukiwania: {e}")
            return []