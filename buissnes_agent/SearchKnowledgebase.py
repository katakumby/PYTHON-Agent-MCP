import logging
import os
import sys
from typing import List

import numpy as np
from typing import List, Any, Protocol, Dict, Optional
from openai import OpenAI

# Data Source
from DataLoaderLocalFileLoader import DataLoaderLocalFileLoader
from DataLoaderS3FileLoader import DataLoaderS3FileLoader
# Chunkings
from textchunker.LangChainChunker import LangChainChunker
from textchunker.NoLibChunker import NoLibChunker as LegacyChunker
# Data base
# from QdrantDatabaseStore import QdrantDatabaseStore

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


# ==============================================================================
# DEFINICJA INTERFEJSU (KONTRAKTU)
# ==============================================================================
# Ten interfejs definiuje wymagania, jakie SearchKnowledgebase stawia bazie danych.
# Musi pasować do metod zdefiniowanych w QdrantDatabaseStore.
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
# KLASA ORKIESTRATORA
# ==============================================================================


class SearchKnowledgebase:
    """
    ### Klasa Orkiestrator (Coordinator Class) - Wersja Zrefaktoryzowana

    Realizuje proces w 3 krokach:
    1. **Setup Danych:** Wybór odpowiedniego Loadera (S3 lub Local).
    2. **Setup Logiki:** Wybór odpowiedniego Chunkera (ContentChunker lub Legacy).
    3. **Execution (Pipeline):** Jednolita pętla przetwarzania (Load -> Chunk -> Embed -> Store).
    """

    def __init__(
            self,
            client: OpenAI,
            input_directory: str,
            input_s3_directory: str,
            database_store: VectorStoreInterface,
            embedding_model: str,
            chunk_module: str,
            chunk_strategy: str,
            data_source_type: str,
            chunk_size: int = 600,
            batch_size: int = 50,
            force_refresh: bool = False
    ):
        self.client = client
        self.store = database_store
        self.model = embedding_model
        self.batch_size = batch_size
        self.chunk_module_type = chunk_module
        self.data_source_type = data_source_type

        # Konfiguracja ścieżek
        self.input_directory = input_directory
        self.input_s3_directory = input_s3_directory
        self.s3_bucket = os.getenv("S3_BUCKET")

        # ======================================================================
        # ETAP 1: Inicjalizacja Warstwy Danych (Loader Strategy)
        # ======================================================================
        # Decydujemy, czy dane będą płynąć z S3 czy z dysku lokalnego.
        # Wynikiem jest obiekt `self.data_loader`, który ma zawsze te same metody.
        self.data_loader = self._initialize_loader(data_source_type)

        # ======================================================================
        # ETAP 2: Inicjalizacja Warstwy Logiki (Chunking Strategy)
        # ======================================================================
        # Decydujemy, jaki silnik będzie ciął tekst.
        # Wynikiem jest obiekt `self.chunker_engine`.
        self.chunker_engine = self._initialize_chunker(chunk_module, chunk_strategy, chunk_size)

        # ======================================================================
        # ETAP 3: Weryfikacja i Uruchomienie
        # ======================================================================
        count = self.store.count()
        logger.info(f"Stan bazy wektorowej: {count} dokumentów.")

        if count > 0 and not force_refresh:
            logger.info("SKIP: Baza niepusta. Ingestia pominięta.")
        else:
            logger.info("START: Uruchamianie jednolitego procesu ETL...")
            self.perform_ingestion()

    def _initialize_loader(self, data_source_type: str):
        """Fabryka Loaderów: Zwraca obiekt do pobierania danych (S3 lub Local)."""
        if data_source_type == "s3":
            logger.info(f"DATA LAYER: Wybrano S3 Loader. Bucket: {self.s3_bucket}")
            try:
                return DataLoaderS3FileLoader(self.s3_bucket, self.input_s3_directory)
            except ImportError as e:
                logger.error("Brak zależności dla S3 (boto3/chunking_s3).")
                raise e
        else:
            logger.info(f"DATA LAYER: Wybrano Local File Loader. Dir: {self.input_directory}")
            return DataLoaderLocalFileLoader(self.input_directory)

    def _initialize_chunker(self, chunk_module: str, strategy: str, size: int):
        """Fabryka Chunkerów: Zwraca obiekt do przetwarzania tekstu."""
        if chunk_module in ["langchain"]:
            logger.info(f"LOGIC LAYER: Wybrano ContentChunker. Strategia: {strategy}")
            return LangChainChunker(strategy, size, 100)
        else:
            logger.info("LOGIC LAYER: Wybrano Legacy Chunker.")
            return LegacyChunker(strategy, size, 100)

    def _embed(self, text: str) -> List[float]:
        """Wrapper na API OpenAI."""
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

                if not raw_text.strip():
                    continue

                # 3. CHUNKING (Transform)
                # Normalizacja wyników, bo LegacyChunker zwraca list[str], a ContentChunker list[dict]
                processed_chunks = []

                if isinstance(self.chunker_engine, LegacyChunker):
                    # Obsługa starego chunkera
                    ext = os.path.splitext(object_key)[1].lower()
                    raw_list = []
                    if ext in [".xml", ".xsd"]:
                        raw_list = self.chunker_engine.fixed(raw_text)
                    else:
                        raw_list = self.chunker_engine.auto(raw_text)

                    # Konwersja do formatu słownikowego
                    for txt in raw_list:
                        processed_chunks.append({
                            "text": txt,
                            "metadata": file_metadata
                        })
                else:
                    # Obsługa nowego ContentChunker (S3/LangChain)
                    # ContentChunker sam dba o merge metadanych
                    processed_chunks = self.chunker_engine.process_content(raw_text, file_metadata)

                # 4. EMBEDDING & BATCHING (Load)
                for item in processed_chunks:
                    text_content = item["text"]
                    metadata = item["metadata"]

                    vec = self._embed(text_content)

                    batch_items.append({
                        "text": text_content,
                        "vector": vec.tolist(),
                        "metadata": metadata
                    })

                    # Wysłanie paczki
                    if len(batch_items) >= self.batch_size:
                        self.store.insert_batch(batch_items)
                        batch_items = []

                files_processed += 1

            except Exception as e:
                logger.error(f"Błąd przetwarzania pliku {object_key}: {e}")
                continue

        # 5. FINALIZACJA
        if batch_items:
            self.store.insert_batch(batch_items)

        logger.info(f"PROCES ZAKOŃCZONY. Przetworzono plików: {files_processed}")