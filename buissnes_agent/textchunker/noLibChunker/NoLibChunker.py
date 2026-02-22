import hashlib
import logging
import sys
from typing import List, Dict, Any

# Importy z pakietu
from .base import BaseNoLibStrategy
from .strategies import (
    FixedStrategy,
    SentencesStrategy,
    MarkdownStrategy,
    SemanticStrategy
)
from ...MetadataModels import ChunkMetadata

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =========================================================
# KLASA: CHUNKER (LEGACY / BASE / NOLIB)
# =========================================================
#
# ### Architektura: Orchestrator (Context)
#
# **Odpowiedzialność:**
# 1.  **Factory / Router:** Wybiera odpowiednią strategię podziału (`_get_strategy`) na podstawie konfiguracji.
# 2.  **Execution Engine:** Dzieli surowy tekst na mniejsze fragmenty (chunki).
# 3.  **Safety Net:** Wymusza sztywne limity znaków (`_enforce_limit`), jeśli strategia logiczna zawiedzie.
# 4.  **Interface Adapter:** Transformuje surowe stringi do ujednoliconego formatu `List[Dict]`,
#     zgodnego z `LangChainChunker` (dodaje UUID i metadane).
#
# **Kluczowa różnica względem LangChainChunker:**
# Ta klasa nie posiada zewnętrznych zależności (poza opcjonalnym Semantic).
# Jest "lekka", szybka i działa na czystym Pythonie.
# =========================================================
class NoLibChunker:
    def __init__(self, chunk_strategy: str, chunk_size: int = 600, chunk_overlap: int = 100):
        """
        Inicjalizacja Chunkera z wyborem strategii i konfiguracją.

        Args:
            chunk_strategy (str): Nazwa strategii (np. 'auto', 'sentences', 'markdown').
            chunk_size (int): Maksymalna długość fragmentu (w znakach).
            chunk_overlap (int): Liczba znaków nakładania się fragmentów (kontekst).
        """
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        logger.info(
            f"NoLibChunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}, Overlap: {chunk_overlap}")

    def _get_strategy(self, text: str) -> BaseNoLibStrategy:
        """
        ### Heurystyka wybierająca strategię (Router / Factory Method)

        **Jak działa:**
        Na podstawie `self.chunk_strategy` wybiera odpowiednią klasę implementującą `BaseNoLibStrategy`.
        Dla opcji 'auto' analizuje tekst, aby podjąć decyzję dynamicznie.
        """

        # Logika "Auto" - Router
        if self.chunk_strategy == "auto":
            # Analizuje tekst. Jeśli znajdzie strukturę Markdown (nagłówek `# `), używa strategii Markdown.
            if "# " in text:
                return MarkdownStrategy(self.chunk_size, self.chunk_overlap)
            else:
                return SentencesStrategy(self.chunk_size, self.chunk_overlap)

        # Mapowanie nazw na klasy strategii
        if self.chunk_strategy == "fixed":
            return FixedStrategy(self.chunk_size, self.chunk_overlap)
        elif self.chunk_strategy in ["sentences", "by_sentences"]:
            return SentencesStrategy(self.chunk_size, self.chunk_overlap)
        elif self.chunk_strategy in ["markdown", "by_markdown_headers"]:
            return MarkdownStrategy(self.chunk_size, self.chunk_overlap)
        elif self.chunk_strategy == "semanticChunker":
            return SemanticStrategy(self.chunk_size, self.chunk_overlap)
        else:
            # Fallback - domyślnie zdania
            logger.warning(f"Nieznana strategia '{self.chunk_strategy}', używam SentencesStrategy.")
            return SentencesStrategy(self.chunk_size, self.chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        """
        Główna metoda logiczna (Low-level).
        Deleguje zadanie podziału tekstu do wybranej strategii.
        Zwraca surowe stringi (nie słowniki).
        """
        if not text:
            return []

        strategy = self._get_strategy(text)
        return strategy.split_text(text)

    # =========================================================================
    # METODA: process_content (Unified Interface)
    # =========================================================================
    def process_content(self, content: str, base_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        ### Główny Pipeline Przetwarzania

        Ujednolica interfejs z `LangChainChunker`. Dzięki temu reszta aplikacji
        nie musi wiedzieć, którego chunkera używa.

        **Etapy procesu:**
        1.  **Primary Split:** Wywołanie strategii logicznej (np. sentences/markdown).
        2.  **Safety Net (`_enforce_limit`):** Sprawdzenie, czy chunki nie przekroczyły limitu znaków.
        3.  **Metadata Injection & Formatting:** Opakowanie stringów w słowniki i nadanie UUID.

        Args:
            content (str): Tekst do podziału.
            base_metadata (Dict): Metadane pliku źródłowego (np. nazwa pliku).
        """
        if not content:
            return []

        if base_metadata is None:
            base_metadata = {}

        # 1. Pobieramy surowe stringi ze strategii (mogą być za długie!)
        raw_chunks: List[str] = self.split_text(content)

        # 2. Hard Limit Enforcer (Bezpiecznik)
        # Gwarantuje, że żaden chunk nie przekroczy chunk_size.
        safe_chunks: List[str] = self._enforce_limit(raw_chunks)

        # 3. Formatowanie do ujednoliconego standardu (List[Dict])
        results = []
        for idx, chunk_text in enumerate(safe_chunks):
            # A. Przygotowanie ID
            source_uri = base_metadata.get("source", "unknown")
            unique_str = f"{source_uri}_{idx}_{chunk_text[:20]}"
            chunk_id = hashlib.md5(unique_str.encode("utf-8")).hexdigest()

            # B. Separacja znanych pól od "extra"
            # Wyciągamy znane pola ze słownika loadera, reszta idzie do extra_data
            known_fields = {
                "source": source_uri,
                "title": base_metadata.get("title"),
                "url": base_metadata.get("url"),
                "extension": base_metadata.get("extension"),
                "domain": base_metadata.get("domain"),
                "tags": base_metadata.get("tags", []),
                "page_number": base_metadata.get("page_number")
            }

            # Wszystko co nie jest znane, trafia do extra
            extras = {k: v for k, v in base_metadata.items() if k not in known_fields}

            # C. Instancjalizacja Dataclass
            meta_obj = ChunkMetadata(
                source=known_fields["source"],
                phrase=chunk_text,  # Mandatory content
                phrase_metadata_id=chunk_id,  # Mandatory ID

                # Opcjonalne
                title=known_fields["title"],
                url=known_fields["url"],
                extension=known_fields["extension"],
                domain=known_fields["domain"],
                tags=known_fields["tags"],
                page_number=known_fields["page_number"],

                extra_data=extras
            )

            # D. Budowanie wyniku
            results.append({
                "text": chunk_text,  # Do embeddingu
                "metadata": meta_obj.to_payload()  # Do bazy (płaski słownik)
            })

        return results

    def _enforce_limit(self, chunks: List[str]) -> List[str]:
        """
        ### Metoda pomocnicza: "Bezpiecznik rozmiaru" (Hard Limit Enforcer - NoLib Version)

        **Cel:** Gwarancja techniczna.
        Strategie logiczne (np. Markdown) dbają o kontekst ("nie tnij w połowie sekcji"),
        ale mogą zignorować limit znaków, jeśli sekcja jest ogromna.

        **Działanie:**
        Iteruje po wygenerowanych chunkach. Jeśli chunk > `chunk_size`, tnie go
        na mniejsze kawałki "na sztywno" (Fixed Size Logic).

        **Dlaczego implementacja ręczna?**
        W przeciwieństwie do `LangChainChunker`, tutaj nie importujemy `RecursiveCharacterTextSplitter`,
        aby zachować klasę lekką i niezależną od bibliotek zewnętrznych (Pure Python).
        """
        final_chunks = []

        for chunk in chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                # Jeśli chunk jest za duży -> tniemy pętlą (logika FixedStrategy)
                start = 0
                step = self.chunk_size - self.chunk_overlap

                # Zabezpieczenie przed pętlą nieskończoną (gdyby overlap >= size)
                if step <= 0:
                    step = self.chunk_size

                while start < len(chunk):
                    end = start + self.chunk_size
                    # Wycinamy pod-kawałek
                    sub_chunk = chunk[start:end]
                    final_chunks.append(sub_chunk)

                    # Warunek stopu, jeśli dotarliśmy do końca
                    if end >= len(chunk):
                        break

                    start += step

        return final_chunks
