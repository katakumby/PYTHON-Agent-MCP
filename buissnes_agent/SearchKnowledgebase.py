import logging
import os
import sys
from typing import Dict, Any, Generator, Tuple
from typing import Protocol, List

import numpy as np
from openai import OpenAI

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
        processed_chunks = []

        chunk_module = os.getenv("CHUNKING_MODULE")

        ext = os.path.splitext(object_key)[1].lower()

        if chunk_module in ["langchain"]:

            # Pobranie dedykowanej konfiguracji (Size, Overlap, Strategy)
            chunk_size, chunk_overlap, strategy = self._get_chunk_config_langchain(ext)
            print(f"Plik: {ext}, Chunk: {chunk_size}, Strategia: {strategy}")

            logger.info(f"LOGIC LAYER: Wybrano ContentChunker. Strategia: {strategy}")
            chunker_engine = LangChainChunker(strategy, chunk_size, chunk_overlap)
            processed_chunks = chunker_engine.process_content(raw_text, file_metadata)
        else:

            # Pobranie dedykowanej konfiguracji (Size, Overlap, Strategy)
            chunk_size, chunk_overlap, strategy = self._get_chunk_config_local(ext)
            print(f"Plik: {ext}, Chunk: {chunk_size}, Strategia: {strategy}")

            logger.info("LOGIC LAYER: Wybrano Legacy Chunker.")
            chunker_engine = LegacyChunker(strategy, chunk_size, chunk_overlap)

            if ext in [".xml", ".xsd"]:
                raw_list = chunker_engine.fixed(raw_text)
            else:
                raw_list = chunker_engine.auto(raw_text)

            # Konwersja do formatu słownikowego
            for txt in raw_list:
                processed_chunks.append({
                    "text": txt,
                    "metadata": file_metadata
                })

        return processed_chunks

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

    def _get_chunk_config_langchain(self, ext: str) -> tuple[int, int, str]:
        """
        Pomocnicza metoda dobierająca parametry chunkowania na podstawie rozszerzenia.
        Zwraca (chunk_size, chunk_overlap, strategy).
        """

        match ext:
            case ".xml":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_XML"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_XML"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_XML")

            case ".xsd":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_XSD"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_XSD"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_XSD")

            case ".json":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_JSON"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_JSON"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_JSON")

            case ".txt":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_TXT"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_TXT"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_TXT")

            case ".md":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_MD"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_MD"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_MD")

            case ".pdf":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_PDF"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_PDF"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_PDF")

            case ".docx":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_DOCX"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_DOCX"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_DOCX")

            case ".xlsx":
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_XLSX"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_XLSX"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_XLSX")

            case _:
                # Domyślne ustawienia dla nieznanych plików (Fallback do zmiennych globalnych)
                chunk_size = int(os.getenv("LANGCHAIN_CHUNK_SIZE_DEF"))
                chunk_overlap = int(os.getenv("LANGCHAIN_CHUNK_OVERLAP_DEF"))
                strategy = os.getenv("LANGCHAIN_STRATEGY_DEF")

        return chunk_size, chunk_overlap, strategy

    def _get_chunk_config_local(self, ext: str) -> tuple[int, int, str]:
        """
        Pomocnicza metoda dobierająca parametry chunkowania na podstawie rozszerzenia.
        Zwraca (chunk_size, chunk_overlap, strategy).
        """

        match ext:
            case ".xml":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_XML"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_XML"))
                strategy = os.getenv("LOCAL_STRATEGY_XML")

            case ".xsd":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_XSD"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_XSD"))
                strategy = os.getenv("LOCAL_STRATEGY_XSD")

            case ".json":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_JSON"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_JSON"))
                strategy = os.getenv("LOCAL_STRATEGY_JSON")

            case ".txt":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_TXT"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_TXT"))
                strategy = os.getenv("LOCAL_STRATEGY_TXT")

            case ".md":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_MD"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_MD"))
                strategy = os.getenv("LOCAL_STRATEGY_MD")

            case ".pdf":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_PDF"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_PDF"))
                strategy = os.getenv("LOCAL_STRATEGY_PDF")

            case ".docx":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_DOCX"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_DOCX"))
                strategy = os.getenv("LOCAL_STRATEGY_DOCX")

            case ".xlsx":
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_XLSX"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_XLSX"))
                strategy = os.getenv("LOCAL_STRATEGY_XLSX")

            case _:
                # Domyślne ustawienia dla nieznanych plików (Fallback do zmiennych globalnych)
                chunk_size = int(os.getenv("LOCAL_CHUNK_SIZE_DEF"))
                chunk_overlap = int(os.getenv("LOCAL_CHUNK_OVERLAP_DEF"))
                strategy = os.getenv("LOCAL_STRATEGY_DEF")

        return chunk_size, chunk_overlap, strategy