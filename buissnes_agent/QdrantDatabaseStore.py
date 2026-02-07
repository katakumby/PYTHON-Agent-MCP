import logging
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Distance, Filter, FieldCondition, MatchValue
import hashlib

logger = logging.getLogger(__name__)


class QdrantDatabaseStore:
    def __init__(self, url: str, api_key: str, collection_name: str, vector_size: int = 1536):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(url=url, api_key=api_key)
        self._ensure_collection()

    def _ensure_collection(self):
        """ Tworzy kolekcję tylko jeśli nie istnieje."""
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
        try:
            return self.client.count(collection_name=self.collection_name).count
        except Exception:
            return 0

    def insert_batch(self, items: List[Dict[str, Any]]):
        if not items: return
        points = []

        """
        Generuj ID na podstawie treści chunka (hash). Dzięki temu, jeśli chunk się nie zmienił, 
        nadpisze się w bazie zamiast tworzyć duplikat.
        """
        for item in items:
            # Generowanie deterministycznego ID na podstawie treści i nazwy pliku
            unique_string = f"{item['metadata']['source_file']}_{item['text']}"
            # Tworzymy hash MD5 jako seed dla UUID
            point_id = str(uuid.UUID(hex=hashlib.md5(unique_string.encode('utf-8')).hexdigest()))

            payload = item["metadata"].copy()
            payload["text"] = item["text"]
            points.append(PointStruct(id=point_id, vector=item["vector"], payload=payload))

        # for item in items:
        #     point_id = str(uuid.uuid4())
        #     payload = item["metadata"].copy()
        #     payload["text"] = item["text"]
        #     points.append(PointStruct(id=point_id, vector=item["vector"], payload=payload))

        try:
            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info(f"Zapisano {len(points)} wektorów.")
        except Exception as e:
            logger.error(f"Błąd zapisu: {e}")

    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict]:
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
            )
            return [{"text": p.payload.get("text", ""), "score": p.score} for p in results.points]
        except Exception as e:
            logger.error(f"Błąd wyszukiwania: {e}")
            return []