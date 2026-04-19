import hashlib
import logging
import sys
from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from buissnes_agent.textchunker.langchain.base import ChunkingStrategy
from .strategies import (
    MarkdownHeaderStrategy,
    RecursiveStrategy,
    UnstructuredStrategy,
    SemanticStrategy
)
from ...MetadataModels import ChunkMetadata
from ..source_metadata import (
    SOURCE_CHAR_END_METADATA_KEY,
    SOURCE_CHAR_START_METADATA_KEY,
    SOURCE_ENCODING_METADATA_KEY,
    SOURCE_TEXT_METADATA_KEY,
)

# Importy interfejsu i strategii

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


class LangChainChunker:
    """
    ### Klasa Główna: Orchestrator (Context)

    Odpowiada za transformację surowego tekstu w gotowe do zindeksowania wektory.
    W nowej architekturze pełni rolę "Context" dla wzorca Strategy.

    **Odpowiedzialności:**
    1.  **Factory:** Wybiera odpowiednią klasę strategii na podstawie konfiguracji (`_get_strategy`).
    2.  **Orchestration:** Zarządza przepływem danych (Primary Split -> Metadata -> Secondary Split).
    3.  **Safety Net:** Aplikuje "Hard Limit Enforcer", niezależnie od wybranej strategii.

    **Kluczowa zmiana:**
    Klasa nie zawiera już logiki "jak ciąć tekst" (to robią strategie w osobnych plikach),
    ale "jak zarządzać procesem cięcia".
    """

    def __init__(self, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        logger.info(f"LangChainChunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}")

    def _get_strategy(self) -> ChunkingStrategy:
        """
        Metoda fabryczna (Factory Method).
        Mapuje nazwę strategii (string) na konkretną instancję klasy strategii.
        """
        if self.chunk_strategy == "markdownHeaderTextSplitter":
            return MarkdownHeaderStrategy()
        elif self.chunk_strategy == "unstructuredMarkdownLoaderSingle":
            return UnstructuredStrategy(mode="single")
        elif self.chunk_strategy == "unstructuredMarkdownLoaderElements":
            return UnstructuredStrategy(mode="elements")
        elif self.chunk_strategy == "semanticChunker":
            return SemanticStrategy()
        elif self.chunk_strategy == "recursive":
            return RecursiveStrategy(self.chunk_size, self.chunk_overlap)
        else:
            # Fallback - jeśli strategia nieznana, użyj bezpiecznej rekurencji
            logger.warning(f"Unknown strategy {self.chunk_strategy}, utilizing recursive fallback.")
            return RecursiveStrategy(self.chunk_size, self.chunk_overlap)

    # =========================================================================
    # METODA: process_content (Wspólna metoda łącząca wejścia)
    # =========================================================================
    def process_content(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """
        Zwraca listę słowników gotowych do wektoryzacji i zapisu w bazie danych.
        Struktura: [{"text": "...", "metadata": {"page_number": 1, ...}}]

        ### Główny Pipeline Przetwarzania

        Łączy wybraną strategię podziału z zarządzaniem limitami.

        **Etapy procesu:**
        1.  **Primary Split (Delegacja):** Zlecamy podział wyspecjalizowanej klasie strategii.
        2.  **Metadata Cleanup:** Ujednolicenie kluczy metadanych.
        3.  **Secondary Split (Hard Limit Enforcer):** Sprawdza, czy logiczne chunki nie są za duże.
        4.  **Formatting:** Nadaje unikalne ID i zwraca strukturę słownikową.
        """

        if not documents:
            return []

        # Krok 1: Wybór strategii i wykonanie cięcia (Primary Split)
        # --- Przekazujemy listę dokumentów do split_documents ---
        strategy = self._get_strategy()
        splits: List[Document] = strategy.split_documents(documents)
        self._normalize_split_metadata(splits)

        # Krok 2: Smart Metadata Cleanup
        # Ponieważ metadane pliku zostały już scalone w Orkiestratorze, robimy tu tylko
        # ewentualną naprawę kluczy (np. Langchain czasami tworzy klucz "page" zamiast "page_number").
        # Krok 3: Secondary Split (Hard Limit / Bezpiecznik)
        # Strategie logiczne (Header/Semantic) mogą zwrócić chunk 5000 znaków, jeśli rozdział był długi.
        # Metoda _enforce_limit tnie go na mniejsze kawałki, zachowując metadane.
        final_documents = splits
        if self.chunk_size > 0:
            final_documents = self._enforce_limit(splits)
            self._normalize_split_metadata(final_documents)

        # Krok 4: Formatowanie wyniku
        results = []
        for idx, doc in enumerate(final_documents):

            # A. Pobieranie danych ze scalonych metadanych dokumentu
            meta_dict = doc.metadata
            source_uri = meta_dict.get("source", "unknown")

            # B. Generowanie ID
            content_snippet = doc.page_content[:50]
            unique_str = f"{source_uri}_{idx}_{content_snippet}"
            chunk_id = hashlib.md5(unique_str.encode("utf-8")).hexdigest()

            # C. Separacja pól znanych od "extra"
            # Definiujemy, które klucze mapujemy wprost na dataclass
            known_keys = {
                "source",
                "title",
                "url",
                "extension",
                "domain",
                "tags",
                "page_number",
                "start_byte",
                "end_byte",
            }

            # Wyciągamy known fields
            schema_data = {k: meta_dict.get(k) for k in known_keys}
            start_byte, end_byte = self._resolve_byte_range(meta_dict)
            schema_data["start_byte"] = start_byte
            schema_data["end_byte"] = end_byte

            # Ustawiamy domyślne source jeśli puste
            if not schema_data["source"]:
                schema_data["source"] = "unknown"

            # Wszystko inne trafia do extras (np. specyficzne metadane z PDF)
            # Pomijamy klucze techniczne, które generujemy sami lub są śmieciami
            exclude_keys = known_keys | {
                "phrase",
                "phrase_metadata_id",
                "_chunk_id",
                "loc",
                "start_index",
                SOURCE_TEXT_METADATA_KEY,
                SOURCE_ENCODING_METADATA_KEY,
                SOURCE_CHAR_START_METADATA_KEY,
                SOURCE_CHAR_END_METADATA_KEY,
            }
            extras = {k: v for k, v in meta_dict.items() if k not in exclude_keys}

            # D. Instancjalizacja Dataclass
            meta_obj = ChunkMetadata(
                source=schema_data["source"],
                phrase=doc.page_content,  # Treść dokumentu
                phrase_metadata_id=chunk_id,  # ID

                title=schema_data["title"],
                url=schema_data["url"],
                extension=schema_data["extension"],
                domain=schema_data["domain"],
                tags=schema_data["tags"] or [],
                page_number=schema_data["page_number"],
                start_byte=schema_data["start_byte"],
                end_byte=schema_data["end_byte"],

                extra_data=extras
            )

            # E. Wynik
            results.append({
                "text": doc.page_content,  # Do embeddingu
                "metadata": meta_obj.to_payload()  # Do bazy (płaskie)
            })

        return results

    def _enforce_limit(self, documents: List[Document]) -> List[Document]:
        """
        ### Metoda pomocnicza: "Bezpiecznik rozmiaru" (Hard Limit Enforcer)

        **Cel:** Gwarancja techniczna.
        Strategie logiczne dbają o kontekst ("nie tnij w połowie zdania"), ale mogą ignorować limit znaków.
        Ta metoda jest wspólna dla wszystkich strategii i działa jako "ostatnia linia obrony".

        Jeśli chunk jest większy niż `self.chunk_size`, używamy "nożyczek precyzyjnych"
        (RecursiveCharacterTextSplitter) aby go dociąć.
        """
        final_docs = []

        # Używamy Recursive jako uniwersalnej metody docinania
        recursive_cutter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],  # Hierarchia cięcia
            add_start_index=True,
            strip_whitespace=False,
        )

        for doc in documents:
            if len(doc.page_content) > self.chunk_size:
                # Jeśli za duży -> tniemy rekurencyjnie
                # Metoda split_documents automatycznie kopiuje metadane rodzica do dzieci
                sub_docs = recursive_cutter.split_documents([doc])
                final_docs.extend(sub_docs)
            else:
                # Jeśli mieści się w limicie -> przepuszczamy bez zmian
                final_docs.append(doc)

        return final_docs

    def _normalize_split_metadata(self, documents: List[Document]) -> None:
        for doc in documents:
            if "page" in doc.metadata:
                if doc.metadata.get("page_number") is None:
                    doc.metadata["page_number"] = doc.metadata.pop("page")
                else:
                    doc.metadata.pop("page")

            local_start = doc.metadata.pop("start_index", None)
            source_char_start = doc.metadata.get(SOURCE_CHAR_START_METADATA_KEY)
            if isinstance(local_start, int) and isinstance(source_char_start, int):
                global_start = source_char_start + local_start
                doc.metadata[SOURCE_CHAR_START_METADATA_KEY] = global_start
                doc.metadata[SOURCE_CHAR_END_METADATA_KEY] = (
                    global_start + len(doc.page_content)
                )

    def _resolve_byte_range(
        self, metadata: Dict[str, Any]
    ) -> tuple[int | None, int | None]:
        source_text = metadata.get(SOURCE_TEXT_METADATA_KEY)
        source_encoding = metadata.get(SOURCE_ENCODING_METADATA_KEY)
        start_char = metadata.get(SOURCE_CHAR_START_METADATA_KEY)
        end_char = metadata.get(SOURCE_CHAR_END_METADATA_KEY)

        if not isinstance(source_text, str):
            return None, None
        if not isinstance(source_encoding, str):
            return None, None
        if not isinstance(start_char, int) or not isinstance(end_char, int):
            return None, None
        if start_char < 0 or end_char <= start_char:
            return None, None

        try:
            start_byte = len(source_text[:start_char].encode(source_encoding))
            end_byte = len(source_text[:end_char].encode(source_encoding)) - 1
        except UnicodeEncodeError:
            return None, None

        if end_byte < start_byte:
            return None, None

        return start_byte, end_byte
