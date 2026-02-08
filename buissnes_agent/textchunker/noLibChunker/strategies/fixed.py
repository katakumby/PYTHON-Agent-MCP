from typing import List
from ..base import BaseNoLibStrategy


class FixedStrategy(BaseNoLibStrategy):
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

    **Implementacja:**
    Ta strategia oblicza overlap matematycznie w pętli `while`, więc nie korzysta
    z metody pomocniczej `_apply_overlap`.
    """

    def split_text(self, text: str) -> List[str]:
        chunks = []
        start = 0

        # Obliczamy krok przesunięcia okna
        step = self.chunk_size - self.chunk_overlap
        if step <= 0:
            step = self.chunk_size  # Zabezpieczenie przed pętlą nieskończoną

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += step

        return chunks