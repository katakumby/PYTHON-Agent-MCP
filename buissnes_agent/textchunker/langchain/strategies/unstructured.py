import os
import tempfile
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from buissnes_agent.textchunker.langchain.base import ChunkingStrategy

class UnstructuredStrategy(ChunkingStrategy):
    """
    ### Strategia 3: Unstructured Library

    Wykorzystuje zewnętrzną bibliotekę do inteligentnego parsowania Markdown.
    Potrafi rozpoznać listy, tabelki i stopki lepiej niż zwykły regex.

    **Zarządzanie zasobami:**
    Biblioteka `unstructured` operuje na plikach na dysku. Ta klasa hermetyzuje (ukrywa)
    całą logikę tworzenia i usuwania plików tymczasowych (tempfile), dzięki czemu
    główna klasa Orchestrator pozostaje czysta.

    **Modes:**
    - 'single': Cały tekst jako jeden element (z wyczyszczonym formatowaniem).
    - 'elements': Dzieli na logiczne elementy (Title, NarrativeText, ListItem).
    """

    def __init__(self, mode: str = "single"):
        self.mode = mode

    def split_text(self, text: str) -> List[Document]:
        suffix = ".md"
        # Tworzenie pliku tymczasowego - wymagane przez bibliotekę Unstructured
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(text.encode("utf-8"))
            temp_file_path = temp_file.name

        try:
            loader = UnstructuredMarkdownLoader(temp_file_path, mode=self.mode)
            return loader.load()
        finally:
            # Sprzątanie po sobie (usuwanie pliku tymczasowego)
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)