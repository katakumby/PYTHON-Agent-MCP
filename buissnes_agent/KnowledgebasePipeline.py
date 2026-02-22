import logging
import os
import sys
from typing import Dict, Any, Generator, Tuple
from typing import Protocol, List

import numpy as np
from openai import OpenAI

from buissnes_agent.config_loader import settings
# Chunkings
from buissnes_agent.textchunker.langchain.LangChainChunker import LangChainChunker
from buissnes_agent.textchunker.noLibChunker.NoLibChunker import NoLibChunker as LegacyChunker

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


# ==============================================================================
# DEFINICJA INTERFEJSU (KONTRAKTU)
# ==============================================================================
# Ten interfejs definiuje wymagania, jakie SearchKnowledgebase stawia bazie danych.
# Musi pasować do metod zdefiniowanych w danym pliku bazy danych.
class VectorStoreInterface(Protocol):

    def count(self) -> int:
        """Zwraca liczbę wektorów w bazie."""
        ...

    def insert_batch(self, items: List[Dict[str, Any]]) -> None:
        """
        Wstawia paczkę dokumentów.
        items: Lista słowników zawierających klucze 'text', 'vector', 'metadata'.
        """
        ...

    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict]:
        """
        Wyszukuje podobne wektory.
        Zwraca listę wyników (słowniki z 'text' i 'score').
        """
        ...


# ==============================================================================
# INTERFEJS 2: ŹRÓDŁO DANYCH (Data Loader)
# ==============================================================================
class DataLoaderInterface(Protocol):
    """
    Abstrakcja źródła danych.
    Ujednolica sposób pobierania plików z S3 (DataLoaderS3FileLoader)
    oraz z dysku lokalnego (DataLoaderLocalFileLoader).
    """

    def list_objects(self) -> Generator[str, None, None]:
        """
        Zwraca generator kluczy/ścieżek do plików.
        """
        ...

    def load_file_with_metadata(self, key: str) -> Tuple[str, Dict[str, Any]]:
        """
        Pobiera treść pliku i jego metadane na podstawie klucza.
        Returns: (raw_text, metadata_dict)
        """
        ...


# ==============================================================================
# KLASA ORKIESTRATORA
# ==============================================================================


class SearchKnowledgebase:
    """
    ### Klasa Orkiestrator (Coordinator Class)

    Realizuje proces w 3 krokach:
    1. **Setup Danych:** Wybór odpowiedniego Loadera (S3 lub Local).
    2. **Setup Logiki:** Wybór odpowiedniego Chunkera (ContentChunker lub Legacy).
    3. **Execution (Pipeline):** Jednolita pętla przetwarzania (Load -> Chunk -> Embed -> Store).
    """

    def __init__(
            self,
            client: OpenAI,
            database_store: VectorStoreInterface,
            data_loader: DataLoaderInterface,
            embedding_model: str,
            batch_size: int = 50,
            force_refresh: bool = False
    ):
        self.client = client
        self.store = database_store
        self.model = embedding_model
        self.batch_size = batch_size
        self.data_loader = data_loader

        # ======================================================================
        # ETAP Weryfikacja i Uruchomienie
        # ======================================================================
        count = self.store.count()
        logger.info(f"Stan bazy wektorowej: {count} dokumentów.")

        if count > 0 and not force_refresh:
            logger.info("SKIP: Baza niepusta. Ingestia pominięta.")
        else:
            logger.info("START: Uruchamianie jednolitego procesu ETL...")
            self.perform_ingestion()

    def _embed(self, text: str) -> List[float]:
        # Wrapper na API OpenAI.
        try:
            emb = self.client.embeddings.create(input=[text.replace("\n", " ")], model=self.model)
            return np.array(emb.data[0].embedding, dtype=np.float32)
        except Exception as e:
            logger.error(f"Embedding API Error: {e}")
            raise e

    def perform_ingestion(self):
        """
        ### Główna Pętla ETL (Unified Pipeline)

        Dzięki abstrakcji Loaderów i Chunkerów, ta metoda jest identyczna
        dla plików lokalnych i S3.
        """
        batch_items = []
        files_processed = 0

        # 1. ITERACJA (Extract)
        # Loader dostarcza strumień plików (ścieżek/kluczy)
        object_generator = self.data_loader.list_objects()

        for object_key in object_generator:
            logger.info(f"Processing: {object_key}")

            try:
                # 2. POBRANIE (Extract)
                # Loader zwraca surowy tekst i metadane pliku
                raw_text, file_metadata = self.data_loader.load_file_with_metadata(object_key)

                if not raw_text or not raw_text.strip():
                    continue

                # 3. CHUNKING (Transform)
                processed_chunks = self._transform_to_chunks(object_key, raw_text, file_metadata)

                # 4. EMBEDDING & BATCHING (Load)
                # Przekazujemy batch_items przez referencję (lista jest mutowalna)
                self._embed_and_queue_batch(processed_chunks, batch_items)

                files_processed += 1

            except Exception as e:
                logger.error(f"Błąd przetwarzania pliku {object_key}: {e}")
                continue

        # 5. FINALIZACJA
        if batch_items:
            self.store.insert_batch(batch_items)

        logger.info(f"PROCES ZAKOŃCZONY. Przetworzono plików: {files_processed}")

    def _transform_to_chunks(self, object_key: str, raw_text: str, file_metadata: dict) -> list[dict]:
        """
        Transformuje surowy tekst na listę chunków ze zunifikowanymi metadanymi.
        Obsługuje zarówno LegacyChunker jak i nowe podejście.
        """

        chunk_module = settings.get("chunking.module")

        ext = os.path.splitext(object_key)[1].lower()

        if chunk_module in ["langchain"]:

            # Pobranie dedykowanej konfiguracji (Size, Overlap, Strategy)
            chunk_size, chunk_overlap, strategy = self._get_chunk_config(chunk_module, ext)
            print(f"Plik: {ext}, Chunk: {chunk_size}, Strategia: {strategy}")

            logger.info(f"LOGIC LAYER: Wybrano ContentChunker. Strategia: {strategy}")
            chunker_engine = LangChainChunker(strategy, chunk_size, chunk_overlap)

        else:

            # Pobranie dedykowanej konfiguracji (Size, Overlap, Strategy)
            chunk_size, chunk_overlap, strategy = self._get_chunk_config(chunk_module, ext)
            print(f"Plik: {ext}, Chunk: {chunk_size}, Strategia: {strategy}")

            logger.info("LOGIC LAYER: Wybrano Legacy Chunker.")
            chunker_engine = LegacyChunker(strategy, chunk_size, chunk_overlap)

        return chunker_engine.process_content(raw_text, file_metadata)

    def _embed_and_queue_batch(self, processed_chunks: list[dict], batch_items: list[dict]) -> None:
        """
        Generuje embeddingi dla chunków i dodaje je do kolejki (batch).
        Jeśli kolejka osiągnie limit, wysyła dane do bazy i czyści kolejkę.

        UWAGA: batch_items jest modyfikowane w miejscu (in-place).
        """
        for item in processed_chunks:
            text_content = item["text"]
            metadata = item["metadata"]

            # Generowanie wektora
            vec = self._embed(text_content)

            batch_items.append({
                "text": text_content,
                "vector": vec.tolist(),
                "metadata": metadata
            })

            # Sprawdzenie wielkości paczki i wysyłka
            if len(batch_items) >= self.batch_size:
                self.store.insert_batch(batch_items)
                batch_items.clear()  # Czyścimy listę, co wpływa na zmienną w głównej funkcji

    def _get_chunk_config(self, module_name: str, ext: str) -> tuple[int, int, str]:
        """
        Uniwersalna metoda pobierająca konfigurację chunkowania z obiektu settings.
        Zastępuje hardkodowane match/case.

        Logika:
        1. Szuka konfiguracji w: chunking.strategies.{module_name}.{ext_bez_kropki}
        2. Jeśli brak, szuka w: chunking.strategies.{module_name}.def (fallback modułu)
        3. Pobiera parametry, uzupełniając braki globalnymi wartościami domyślnymi.
        """

        # Usuwamy kropkę z rozszerzenia, bo w YAML klucze jej nie mają (np. "json", a nie ".json")
        clean_ext = ext.lstrip(".").lower()
        if not clean_ext:
            clean_ext = "def"

        # Ścieżka bazowa w konfiguracji dla danego modułu
        base_path = f"chunking.strategies.{module_name}"

        # Próba pobrania konfiguracji dla konkretnego rozszerzenia
        # np. chunking.strategies.langchain.xml
        ext_config = settings.get(f"{base_path}.{clean_ext}")

        # Jeśli nie znaleziono konfiguracji dla rozszerzenia, użyj domyślnej dla modułu (.def)
        if not ext_config:
            logger.debug(f"Brak strategii dla {clean_ext} w module {module_name}. Używam fallbacku 'def'.")
            ext_config = settings.get(f"{base_path}.def")

        # Jeśli nadal nic nie ma (nawet .def w module nie istnieje), użyj pustego słownika,
        # co spowoduje pobranie globalnych wartości domyślnych poniżej.
        if not ext_config:
            logger.warning(f"CRITICAL: Brak konfiguracji fallback 'def' dla modułu {module_name}!")
            ext_config = {}

        # Pobieranie wartości z fallbackiem do globalnych ustawień 'chunking.default_size' itp.
        # YAML: chunking.default_size
        global_default_size = settings.get("chunking.default_size")
        global_default_overlap = settings.get("chunking.default_overlap")

        chunk_size = ext_config.get("size", global_default_size)
        chunk_overlap = ext_config.get("overlap", global_default_overlap)

        # Strategia musi być zdefiniowana, jeśli nie - bezpieczny fallback
        strategy = ext_config.get("strategy", "recursive" if module_name == "langchain" else "auto")

        return int(chunk_size), int(chunk_overlap), str(strategy)