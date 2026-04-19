from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from buissnes_agent.textchunker.langchain.base import ChunkingStrategy

class RecursiveStrategy(ChunkingStrategy):
    """
    ### Strategia 2: Recursive (Mechaniczna / Fallback)

    Klasyczna metoda dzielenia tekstu. Próbuje dzielić wg hierarchii separatorów:
    1. Akapity (\\n\\n)
    2. Linie (\\n)
    3. Zdania (.)

    **Zastosowanie:**
    Używana jako główna strategia (gdy zależy nam tylko na rozmiarze) lub jako fallback,
    gdy inne metody zawiodą. Gwarantuje, że chunk nie przekroczy zadanego rozmiaru.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[Document]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            add_start_index=True,
            strip_whitespace=False,
        )
        # MAGIA: split_documents potnie tekst zachowując numer strony (metadane) z dokumentu wejściowego!
        return text_splitter.split_documents(documents)
