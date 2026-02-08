import os
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

from buissnes_agent.textchunker.langchain.base import ChunkingStrategy

class SemanticStrategy(ChunkingStrategy):
    """
    ### Strategia 4: Semantic Chunking (Znaczeniowa / AI)

    Najbardziej zaawansowana metoda. Nie patrzy na znaki nowej linii czy nagłówki.
    Analizuje wektory (embeddingi) zdań.

    **Jak działa:**
    1. Zamienia zdania na liczby (wektory).
    2. Oblicza podobieństwo między sąsiednimi zdaniami.
    3. Jeśli podobieństwo spada poniżej progu (breakpoint threshold), uznaje to za zmianę tematu i robi cięcie.

    **Optymalizacja:**
    Inicjalizacja modelu OpenAI Embeddings odbywa się teraz wewnątrz tej klasy.
    Dzięki temu, jeśli użytkownik wybierze strategię "Recursive", nie marnujemy zasobów
    na łączenie się z API OpenAI.
    """

    def __init__(self):
        # Konfiguracja Embeddingów (Inicjalizowana tylko wewnątrz tej strategii)
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('EMBEDDING_BASE_URL'),
            api_key=os.getenv('EMBEDDING_API_KEY'),
            check_embedding_ctx_length=False
        )

    def split_text(self, text: str) -> List[Document]:
        if not self.embeddings:
            raise ValueError("Embeddings not initialized. Check env vars.")

        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,  # Wysoki próg - tnie tylko przy wyraźnej zmianie tematu
            min_chunk_size=200
        )
        return text_splitter.create_documents([text])