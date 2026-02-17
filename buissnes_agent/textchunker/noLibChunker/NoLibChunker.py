import logging
import sys
import uuid
from typing import List, Dict, Any

# Importy z pakietu
from .base import BaseNoLibStrategy

from .strategies import (
    FixedStrategy,
    SentencesStrategy,
    MarkdownStrategy,
    SemanticStrategy
)

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
        for chunk_text in safe_chunks:
            # Kopiujemy metadane bazowe, żeby nie nadpisywać ich w pętli
            chunk_metadata = base_metadata.copy()

            # Generujemy unikalne ID dla chunka (niezbędne dla baz wektorowych)
            if "_chunk_id" not in chunk_metadata:
                chunk_metadata["_chunk_id"] = str(uuid.uuid4())

            results.append({
                "text": chunk_text,
                "metadata": chunk_metadata
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
