import logging
import re
import sys
import os
from typing import List

# Dodano import niezbędny do obsługi strategii semanticChunker w __init__
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    # Fallback, aby kod nie wywalił się przy imporcie, jeśli ktoś nie ma langchain
    OpenAIEmbeddings = None

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# =========================================================
# KLASA: CHUNKER (LEGACY / BASE)
# =========================================================
# Odpowiedzialność:
# Dzieli surowy tekst na mniejsze fragmenty (chunki).
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
        self.embeddings = None

        if self.chunk_strategy == "semanticChunker":
            if OpenAIEmbeddings is None:
                logger.error("Brak biblioteki langchain_openai! Nie można użyć strategii semanticChunker.")
            else:
                self.embeddings = OpenAIEmbeddings(
                    model=os.getenv('EMBEDDING_MODEL'),
                    base_url=os.getenv('EMBEDDING_BASE_URL'),
                    api_key=os.getenv('EMBEDDING_API_KEY'),
                    check_embedding_ctx_length=False
                )

        logger.info(
            f"Chunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}, Overlap: {chunk_overlap}")

    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """
        ### Metoda pomocnicza: Ręczna obsługa Overlapu

        **Co robi:**
        Bierze listę pociętych fragmentów i dokleja końcówkę poprzedniego fragmentu
        na początek bieżącego.

        **Dlaczego:**
        Większość prostych metod podziału (np. split by regex) ucina kontekst.
        Dzięki overlapowi, jeśli zdanie jest przecięte między chunkami,
        model AI ma szansę zobaczyć jego brakującą część w sąsiednim chunku.
        """

        if self.chunk_overlap <= 0 or len(chunks) < 2:
            return chunks
        overlapped = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped.append(chunk)
            else:
                # Pobieramy końcówkę poprzedniego chunka
                overlap = chunks[i - 1][-self.chunk_overlap:]
                overlapped.append(overlap + " " + chunk)
        return overlapped

    def fixed(self, text: str) -> List[str]:
        """
        ### Strategia 1: Fixed Size (Sztywny podział)

        **Jak działa:**
        Iteruje po tekście i wycina fragmenty o stałej długości (np. 600 znaków),
        przesuwając okno o (chunk_size - chunk_overlap).

        **Zastosowanie:**
        Pliki binarne, hex, base64 lub bardzo "brudne" dane, gdzie podział na zdania
        nie ma sensu lub jest niemożliwy.

        **Wada:**
        Przecina słowa w połowie, co może utrudnić zrozumienie przez LLM.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def by_sentences(self, text: str) -> List[str]:
        """
        ### Strategia 2: Sentence Split (Podział na zdania)

        **Jak działa:**
        1. Używa Regex do znalezienia końców zdań (.!?).
        2. Iteruje po zdaniach i skleja je w jeden chunk, dopóki nie przekroczy `chunk_size`.
        3. Gdy limit jest osiągnięty, zamyka chunk i zaczyna nowy.
        4. Na końcu aplikuje overlap za pomocą `_apply_overlap`.

        **Zastosowanie:**
        Zwykły tekst, artykuły, e-maile. Dużo lepsze niż `fixed` bo nie tnie słów.
        """

        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks, current = [], ""
        for sentence in sentences:
            if len(current) + len(sentence) <= self.chunk_size:
                current += " " + sentence
            else:
                chunks.append(current.strip())
                current = sentence
        if current.strip():
            chunks.append(current.strip())
        return self._apply_overlap(chunks)

    def by_markdown_headers(self, text: str) -> List[str]:
        """
        ### Strategia 3: Markdown Headers (Regex)

        **Jak działa:**
        Używa Regex (multiline), aby znaleźć nagłówki Markdown (#, ##, ###).
        Dzieli tekst w miejscach wystąpienia nagłówka.

        **Zastosowanie:**
        Dokumentacja techniczna, README.md. Pozwala zachować logiczną spójność sekcji.
        """

        blocks = re.split(r'(?=^#{1,3}\s)', text, flags=re.MULTILINE)
        blocks = [b.strip() for b in blocks if b.strip()]
        return self._apply_overlap(blocks)

    def auto(self, text: str) -> List[str]:
        """
        ### Heurystyka wybierająca strategię (Router)

        **Jak działa:**
        Analizuje tekst. Jeśli znajdzie strukturę Markdown (nagłówek `# `),
        używa strategii Markdown. W przeciwnym razie używa podziału na zdania.
        To domyślna metoda, jeśli strategia to 'auto'.
        """

        if "# " in text: return self.by_markdown_headers(text)
        return self.by_sentences(text)