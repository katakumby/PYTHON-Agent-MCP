import logging
import re
import sys
from typing import List

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')

# =========================================================
# KLASA: CHUNKER (LEGACY)
# =========================================================
# Odpowiedzialność:
# Dzieli surowy tekst na mniejsze fragmenty (chunki).
# =========================================================
class Chunker:
    def __init__(self, chunk_size=600, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        if self.chunk_overlap <= 0 or len(chunks) < 2:
            return chunks
        overlapped = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped.append(chunk)
            else:
                overlap = chunks[i - 1][-self.chunk_overlap:]
                overlapped.append(overlap + " " + chunk)
        return overlapped

    def fixed(self, text: str) -> List[str]:
        """Strategia 1: Fixed Size (Sztywny podział)."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def by_sentences(self, text: str) -> List[str]:
        """Strategia 2: Sentence Split (Podział na zdania)."""
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
        """Strategia 4: Markdown Headers."""
        blocks = re.split(r'(?=^#{1,3}\s)', text, flags=re.MULTILINE)
        blocks = [b.strip() for b in blocks if b.strip()]
        return self._apply_overlap(blocks)

    def auto(self, text: str) -> List[str]:
        """Heurystyka wybierająca strategię."""
        if "# " in text: return self.by_markdown_headers(text)
        return self.by_sentences(text)