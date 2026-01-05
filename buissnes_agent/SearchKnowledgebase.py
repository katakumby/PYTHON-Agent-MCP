import logging
import os
import sys

import numpy as np
from openai import OpenAI

from chunking_base import Chunker as LegacyChunker
from chunking_lang_graph import AdvancedChunker as LangChainChunker
# USUNIĘTO: from chunking_s3 import S3Chunker <- To powodowało błąd braku boto3 przy starcie
from vector_store import QdrantStore

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


class SearchKnowledgebase:
    def __init__(
            self,
            client: OpenAI,
            input_directory: str,
            vector_store: QdrantStore,
            embedding_model: str,
            chunk_module: str = "legacy",
            chunk_strategy: str = "auto",
            chunk_size: int = 600,
            batch_size: int = 50,
            force_refresh: bool = False
    ):
        self.client = client
        self.input_directory = input_directory
        self.store = vector_store
        self.model = embedding_model
        self.batch_size = batch_size
        self.chunk_module_type = chunk_module

        # INICJALIZACJA CHUNKERÓW
        if chunk_module == "langchain":
            logger.info(f"CHUNKER: Moduł LangChain. Strategia: {chunk_strategy}")
            self.chunker_instance = LangChainChunker(chunk_strategy, chunk_size, 100)

        elif chunk_module == "s3":
            # --- LAZY IMPORT ---
            # Importujemy tylko wtedy, gdy wybrano tryb S3.
            # Dzięki temu nie wywali błędu braku 'boto3' w trybie lokalnym.
            try:
                from chunking_s3 import S3Chunker
            except ImportError as e:
                logger.error("Wybrano moduł S3, ale brakuje bibliotek! Zainstaluj: pip install boto3 unstructured")
                raise e

            bucket = os.getenv("S3_BUCKET")
            logger.info(f"CHUNKER: Moduł S3. Bucket: {bucket}, Prefix: {input_directory}, Strategia: {chunk_strategy}")

            self.chunker_instance = S3Chunker(
                bucket_name=bucket,
                prefix=input_directory,
                chunk_strategy=chunk_strategy,
                chunk_size=chunk_size,
                chunk_overlap=100
            )

        else:
            logger.info(f"CHUNKER: Moduł Legacy. Strategia: Auto")
            self.chunker_instance = LegacyChunker(chunk_size, 100)

        # Sprawdzenie bazy
        count = self.store.count()
        logger.info(f"Stan bazy przed startem: {count} dokumentów.")

        if count > 0 and not force_refresh:
            logger.info("Baza nie jest pusta. Pomijam ingestie.")
        else:
            logger.info("Rozpoczynam proces ingestii (ETL)...")
            if chunk_module == "s3":
                self._process_and_ingest_s3()
            else:
                self._process_and_ingest()

    def _perform_chunking(self, text: str, ext: str) -> list[str]:
        # Ta metoda jest używana tylko dla local files (legacy/langchain)
        if self.chunk_module_type == "langchain":
            return self.chunker_instance.split_text(text)
        else:
            if ext in [".xml", ".xsd"]: return self.chunker_instance.fixed(text)
            return self.chunker_instance.auto(text)

    def _read_text_file(self, path):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Błąd odczytu {path}: {e}")
            return ""

    def _embed(self, text):
        emb = self.client.embeddings.create(input=[text.replace("\n", " ")], model=self.model)
        return np.array(emb.data[0].embedding, dtype=np.float32)

    # --- ETL Process Local ---
    def _process_and_ingest(self):
        abs_path = os.path.abspath(self.input_directory)
        logger.info(f"Szukam plików lokalnych w katalogu: {abs_path}")

        if not os.path.exists(abs_path):
            logger.error(f"KATALOG NIE ISTNIEJE! {self.input_directory}")
            return

        batch_items = []
        files_processed = 0

        for root, _, files in os.walk(abs_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                content = ""
                if ext in [".md", ".txt", ".xml", ".xsd"]:
                    content = self._read_text_file(file_path)
                else:
                    continue

                if not content.strip(): continue

                chunks = self._perform_chunking(content, ext)

                for i, chunk in enumerate(chunks):
                    try:
                        vec = self._embed(chunk)
                        batch_items.append({
                            "text": chunk,
                            "vector": vec.tolist(),
                            "metadata": {"source_file": file}
                        })
                    except Exception as e:
                        logger.error(f"Błąd embeddingu: {e}")

                    if len(batch_items) >= self.batch_size:
                        self.store.insert_batch(batch_items)
                        batch_items = []

                files_processed += 1

        if batch_items:
            self.store.insert_batch(batch_items)
        logger.info(f"Zakończono ETL Local. Przetworzono: {files_processed}.")

    # --- ETL Process S3 ---
    def _process_and_ingest_s3(self):
        logger.info("Rozpoczynam pobieranie i przetwarzanie plików z S3...")

        batch_items = []
        files_processed = 0

        # self.chunker_instance tutaj jest na pewno S3Chunker (zainicjowany w __init__)
        for s3_key in self.chunker_instance.list_objects():
            logger.info(f"Przetwarzanie S3: {s3_key}")

            try:
                chunked_docs = self.chunker_instance.process_file(s3_key)

                for item in chunked_docs:
                    text_content = item["text"]
                    metadata = item["metadata"]

                    vec = self._embed(text_content)

                    batch_items.append({
                        "text": text_content,
                        "vector": vec.tolist(),
                        "metadata": metadata
                    })

                    if len(batch_items) >= self.batch_size:
                        logger.info(f"Zapisywanie batcha S3 {len(batch_items)} elementów...")
                        self.store.insert_batch(batch_items)
                        batch_items = []

                files_processed += 1

            except Exception as e:
                logger.error(f"Błąd przetwarzania pliku {s3_key}: {e}")

        if batch_items:
            logger.info(f"Zapisywanie ostatniego batcha S3...")
            self.store.insert_batch(batch_items)

        logger.info(f"Zakończono ETL S3. Przetworzono plików: {files_processed}")