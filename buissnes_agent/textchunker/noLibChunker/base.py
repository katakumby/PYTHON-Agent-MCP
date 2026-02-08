from abc import ABC, abstractmethod
from typing import List


class BaseNoLibStrategy(ABC):
    """
    ### Klasa Bazowa: BaseNoLibStrategy

    Definiuje interfejs dla wszystkich strategii, które nie wymagają ciężkich bibliotek (poza opcjonalnym Semantic).
    Gromadzi wspólną logikę, taką jak obsługa `chunk_overlap`.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """
        Abstrakcyjna metoda, którą musi zaimplementować każda strategia.
        Zwraca listę stringów (nie obiektów Document).
        """
        pass

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

        **Zmiana w refaktoringu:**
        Metoda została przeniesiona do klasy bazowej, aby strategie `Sentences` i `Markdown`
        mogły z niej dziedziczyć bez powielania kodu.
        """
        if self.chunk_overlap <= 0 or len(chunks) < 2:
            return chunks

        overlapped = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped.append(chunk)
            else:
                # Pobieramy końcówkę poprzedniego chunka
                # Zabezpieczenie: bierzemy overlap, ale nie więcej niż długość chunka
                overlap_len = min(len(chunks[i - 1]), self.chunk_overlap)
                overlap = chunks[i - 1][-overlap_len:]
                overlapped.append(overlap + " " + chunk)
        return overlapped