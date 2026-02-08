import logging
import sys
from typing import List

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
# KLASA: CHUNKER (LEGACY / BASE)
# =========================================================
# Odpowiedzialność:
# Dzieli surowy tekst na mniejsze fragmenty (chunki).
# W nowej wersji: Zarządza strategiami podziału (Context Pattern).
# =========================================================
class NoLibChunker:
    def __init__(self, chunk_strategy: str, chunk_size: int = 600, chunk_overlap: int = 100):
        """
        Inicjalizacja Chunkera z wyborem strategii i konfiguracją.

        Args:
            chunk_strategy (str): Nazwa strategii (np. 'auto', 'recursive', 'semanticChunker').
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
        ### Heurystyka wybierająca strategię (Router)

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
        Główna metoda publiczna.
        Deleguje zadanie podziału tekstu do wybranej strategii.
        """
        if not text:
            return []

        strategy = self._get_strategy(text)
        return strategy.split_text(text)

    # --- Metody dla kompatybilności wstecznej (Legacy API) ---
    # Pozwalają wywołać konkretną strategię "ręcznie", tak jak w starej klasie.

    def fixed(self, text: str) -> List[str]:
        """Wywołuje bezpośrednio strategię Fixed."""
        return FixedStrategy(self.chunk_size, self.chunk_overlap).split_text(text)

    def by_sentences(self, text: str) -> List[str]:
        """Wywołuje bezpośrednio strategię Sentences."""
        return SentencesStrategy(self.chunk_size, self.chunk_overlap).split_text(text)

    def by_markdown_headers(self, text: str) -> List[str]:
        """Wywołuje bezpośrednio strategię Markdown Headers."""
        return MarkdownStrategy(self.chunk_size, self.chunk_overlap).split_text(text)

    def auto(self, text: str) -> List[str]:
        """
        Wywołuje logikę automatyczną.
        UWAGA: Ta metoda zmienia wewnętrzny stan strategii na 'auto'.
        """
        self.chunk_strategy = "auto"
        return self.split_text(text)