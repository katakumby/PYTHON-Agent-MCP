import os
import logging
from typing import List
from ..base import BaseNoLibStrategy

# Logger lokalny dla strategii
logger = logging.getLogger(__name__)


class SemanticStrategy(BaseNoLibStrategy):
    """
    ### Strategia 4: Semantic Chunker (LangChain Wrapper)

    To jedyna strategia w pakiecie NoLib, która faktycznie używa biblioteki (LangChain).
    Została tu umieszczona, aby zachować kompatybilność z oryginalnym kodem `NoLibChunker`.

    **Obsługa błędów:**
    Jeśli biblioteka `langchain_openai` nie jest zainstalowana, klasa zaloguje błąd,
    zamiast wywalać całą aplikację przy imporcie.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int):
        super().__init__(chunk_size, chunk_overlap)
        self.splitter = None

        try:
            from langchain_openai import OpenAIEmbeddings
            from langchain_experimental.text_splitter import SemanticChunker

            embeddings = OpenAIEmbeddings(
                model=os.getenv('EMBEDDING_MODEL'),
                base_url=os.getenv('EMBEDDING_BASE_URL'),
                api_key=os.getenv('EMBEDDING_API_KEY'),
                check_embedding_ctx_length=False
            )
            # Inicjalizacja splittera
            self.splitter = SemanticChunker(
                embeddings,
                breakpoint_threshold_type="percentile"
            )
        except ImportError:
            logger.error("Brak biblioteki langchain_openai! Nie można użyć strategii semanticChunker.")
        except Exception as e:
            logger.error(f"Błąd inicjalizacji SemanticStrategy: {e}")

    def split_text(self, text: str) -> List[str]:
        if not self.splitter:
            logger.warning("Semantic splitter nie został zainicjowany. Zwracam tekst bez zmian.")
            return [text]

        # SemanticChunker zwraca obiekty Document, a NoLibChunker oczekuje listy stringów
        docs = self.splitter.create_documents([text])
        return [doc.page_content for doc in docs]