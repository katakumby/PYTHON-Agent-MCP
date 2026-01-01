import logging
import os
import sys

import numpy as np
from openai import OpenAI

from chunking_base import Chunker as LegacyChunker
from chunking_lang_graph import AdvancedChunker as LangChainChunker
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

        if chunk_module == "langchain":
            logger.info(f"CHUNKER: Moduł LangChain. Strategia: {chunk_strategy}")
            self.chunker_instance = LangChainChunker(chunk_strategy, chunk_size, 100)
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
            self._process_and_ingest()

    def _perform_chunking(self, text: str, ext: str) -> list[str]:
        if self.chunk_module_type == "langchain":
            return self.chunker_instance.split_text(text)
        else:
            if ext in [".xml", ".xsd"]: return self.chunker_instance.fixed(text)
            return self.chunker_instance.auto(text)

    # --- Parsery ---
    def _read_text_file(self, path):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Błąd odczytu {path}: {e}")
            return ""

    # --- ETL Process ---
    def _process_and_ingest(self):
        # 1. DIAGNOSTYKA ŚCIEŻKI
        abs_path = os.path.abspath(self.input_directory)
        logger.info(f"Szukam plików w katalogu: {abs_path}")

        if not os.path.exists(abs_path):
            logger.error(f"KATALOG NIE ISTNIEJE! Sprawdź ścieżkę w .env: {self.input_directory}")
            # Spróbujmy podpowiedzieć gdzie szuka
            logger.error(f"Aktualny katalog roboczy to: {os.getcwd()}")
            return

        batch_items = []
        files_found = 0
        files_processed = 0

        for root, _, files in os.walk(abs_path):
            for file in files:
                files_found += 1
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                logger.info(f"Znaleziono plik: {file} ({ext})")

                # Obsługa rozszerzeń
                content = ""
                if ext in [".md", ".txt", ".xml", ".xsd"]:
                    content = self._read_text_file(file_path)
                # (tu można dodać PDF/DOCX jeśli masz biblioteki)
                else:
                    logger.warning(f"Pomijam nieobsługiwany format: {ext}")
                    continue

                if not content.strip():
                    logger.warning(f"Plik jest pusty: {file}")
                    continue

                # Chunking
                chunks = self._perform_chunking(content, ext)
                logger.info(f"Pocięto na {len(chunks)} fragmentów.")

                # Embedding & Batching
                for i, chunk in enumerate(chunks):
                    try:
                        vec = self._embed(chunk)

                        batch_items.append({
                            "text": chunk,
                            "vector": vec.tolist(),
                            "metadata": {"source_file": file}
                        })
                    except Exception as e:
                        logger.error(f"Błąd embeddingu dla fragmentu {i}: {e}")

                    if len(batch_items) >= self.batch_size:
                        logger.info(f"Zapisywanie batcha {len(batch_items)} elementów...")
                        self.store.insert_batch(batch_items)
                        batch_items = []

                files_processed += 1

        # Zapisz resztki
        if batch_items:
            logger.info(f"Zapisywanie ostatniego batcha {len(batch_items)} elementów...")
            self.store.insert_batch(batch_items)

        logger.info(f"Zakończono ETL. Znaleziono: {files_found}, Przetworzono: {files_processed}.")

    def _embed(self, text):
        emb = self.client.embeddings.create(input=[text.replace("\n", " ")], model=self.model)
        return np.array(emb.data[0].embedding, dtype=np.float32)