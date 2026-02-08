from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document


class ChunkingStrategy(ABC):
    """
    ### Klasa Abstrakcyjna: Interfejs Strategii

    Definiuje kontrakt, który musi spełnić każda metoda podziału tekstu.
    Dzięki temu główna klasa (LangChainChunker) nie musi znać szczegółów implementacji
    (np. czy używamy AI, czy regexów), a jedynie wywołuje metodę `split_text`.

    **Rozszerzenie:**
    To fundament wzorca Strategy. Jeśli w przyszłości będziemy chcieli dodać np. podział kodu Python,
    wystarczy dodać nową klasę dziedziczącą po ChunkingStrategy, bez modyfikowania głównego silnika.
    """

    @abstractmethod
    def split_text(self, text: str) -> List[Document]:
        """
        Metoda odpowiedzialna za logiczny podział tekstu na mniejsze fragmenty (Document objects).
        Każda strategia implementuje tę metodę na swój własny sposób.
        """
        pass