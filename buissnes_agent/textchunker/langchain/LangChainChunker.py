import logging
import sys
import uuid
from typing import List, Dict, Any
import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from buissnes_agent.textchunker.langchain.base import ChunkingStrategy
# Importy interfejsu i strategii

from .strategies import (
    MarkdownHeaderStrategy,
    RecursiveStrategy,
    UnstructuredStrategy,
    SemanticStrategy
)

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

class LangChainChunker:
    """
    ### Klasa Główna: Orchestrator (Context)

    Odpowiada za transformację surowego tekstu w gotowe do zindeksowania wektory.
    W nowej architekturze pełni rolę "Context" dla wzorca Strategy.

    **Odpowiedzialności:**
    1.  **Factory:** Wybiera odpowiednią klasę strategii na podstawie konfiguracji (`_get_strategy`).
    2.  **Orchestration:** Zarządza przepływem danych (Primary Split -> Metadata -> Secondary Split).
    3.  **Safety Net:** Aplikuje "Hard Limit Enforcer", niezależnie od wybranej strategii.

    **Kluczowa zmiana:**
    Klasa nie zawiera już logiki "jak ciąć tekst" (to robią strategie w osobnych plikach),
    ale "jak zarządzać procesem cięcia".
    """

    def __init__(self, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        logger.info(f"ContentChunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}")

    def _get_strategy(self) -> ChunkingStrategy:
        """
        Metoda fabryczna (Factory Method).
        Mapuje nazwę strategii (string) na konkretną instancję klasy strategii.
        """
        if self.chunk_strategy == "markdownHeaderTextSplitter":
            return MarkdownHeaderStrategy()
        elif self.chunk_strategy == "unstructuredMarkdownLoaderSingle":
            return UnstructuredStrategy(mode="single")
        elif self.chunk_strategy == "unstructuredMarkdownLoaderElements":
            return UnstructuredStrategy(mode="elements")
        elif self.chunk_strategy == "semanticChunker":
            return SemanticStrategy()
        elif self.chunk_strategy == "recursive":
            return RecursiveStrategy(self.chunk_size, self.chunk_overlap)
        else:
            # Fallback - jeśli strategia nieznana, użyj bezpiecznej rekurencji
            logger.warning(f"Unknown strategy {self.chunk_strategy}, utilizing recursive fallback.")
            return RecursiveStrategy(self.chunk_size, self.chunk_overlap)

    # =========================================================================
    # METODA: process_content (Wspólna metoda łącząca wejścia)
    # =========================================================================
    def process_content(self, content: str, base_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        ### Główny Pipeline Przetwarzania

        Łączy wybraną strategię podziału z zarządzaniem limitami.

        **Etapy procesu:**
        1.  **Primary Split (Delegacja):** Zlecamy podział wyspecjalizowanej klasie strategii.
        2.  **Metadata Injection:** Do każdego powstałego fragmentu doklejane są metadane źródłowe.
        3.  **Secondary Split (Hard Limit Enforcer):** Sprawdza, czy logiczne chunki nie są za duże.
        4.  **Formatting:** Nadaje unikalne ID i zwraca strukturę słownikową.
        """

        # Krok 1: Wybór strategii i wykonanie cięcia (Primary Split)
        # Delegujemy zadanie do odpowiedniej klasy z katalogu 'strategies/'
        strategy = self._get_strategy()
        splits: List[Document] = strategy.split_text(content)

        # Krok 2: Wzbogacenie o metadane źródłowe
        # Metadane z Loadera (np. nazwa pliku) są propagowane do każdego fragmentu tego pliku
        for doc in splits:
            doc.metadata.update(base_metadata)

        # Krok 3: Secondary Split (Hard Limit / Bezpiecznik)
        # Strategie logiczne (Header/Semantic) mogą zwrócić chunk 5000 znaków, jeśli rozdział był długi.
        # Metoda _enforce_limit pocięcie go na mniejsze kawałki, zachowując metadane.
        final_documents = splits
        if self.chunk_size > 0:
            final_documents = self._enforce_limit(splits)

        # Krok 4: Formatowanie wyniku
        results = []
        for idx, doc in enumerate(final_documents):

            # A. Mapowanie PHRASE (Mandatory content)
            # Treść chunka staje się polem 'phrase' w metadanych
            doc.metadata["phrase"] = doc.page_content

            # B. Mapowanie PAGE_NUMBER
            # Niektóre strategie LangChain (np. PDF loader) mogą dodać klucz 'page'.
            # Mapujemy go na wymagany 'page_number'.
            if "page" in doc.metadata:
                doc.metadata["page_number"] = doc.metadata.pop("page")
            elif "page_number" not in doc.metadata:
                doc.metadata["page_number"] = None

            # C. Generowanie PHRASE_METADATA_ID (Mandatory ID)
            # Generujemy deterministyczny hash: Source URI + Index + Fragment treści
            source_uri = doc.metadata.get("source", "unknown")
            # Używamy pierwszych 50 znaków treści do solenia hasha
            content_snippet = doc.page_content[:50]

            unique_str = f"{source_uri}_{idx}_{content_snippet}"
            chunk_id = hashlib.md5(unique_str.encode("utf-8")).hexdigest()

            doc.metadata["phrase_metadata_id"] = chunk_id

            # D. Oczyszczanie (opcjonalne)
            # Usuwamy stare klucze jeśli istnieją, żeby nie śmiecić w bazie
            if "_chunk_id" in doc.metadata:
                del doc.metadata["_chunk_id"]

            # E. Budowanie wyniku dla SearchKnowledgebase
            results.append({
                "text": doc.page_content,  # Służy do generowania wektora (embeddingu)
                "metadata": doc.metadata  # Trafia do Payload w Qdrant (zawiera 'phrase')
            })

        return results

    def _enforce_limit(self, documents: List[Document]) -> List[Document]:
        """
        ### Metoda pomocnicza: "Bezpiecznik rozmiaru" (Hard Limit Enforcer)

        **Cel:** Gwarancja techniczna.
        Strategie logiczne dbają o kontekst ("nie tnij w połowie zdania"), ale mogą ignorować limit znaków.
        Ta metoda jest wspólna dla wszystkich strategii i działa jako "ostatnia linia obrony".

        Jeśli chunk jest większy niż `self.chunk_size`, używamy "nożyczek precyzyjnych"
        (RecursiveCharacterTextSplitter) aby go dociąć.
        """
        final_docs = []

        # Używamy Recursive jako uniwersalnej metody docinania
        # Używamy tutaj bezpośrednio klasy bibliotecznej, a nie naszej strategii,
        # bo potrzebujemy precyzyjnej kontroli nad listą dokumentów.
        recursive_cutter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]  # Hierarchia cięcia
        )

        for doc in documents:
            if len(doc.page_content) > self.chunk_size:
                # Jeśli za duży -> tniemy rekurencyjnie
                # Metoda split_documents automatycznie kopiuje metadane rodzica do dzieci
                sub_docs = recursive_cutter.split_documents([doc])
                final_docs.extend(sub_docs)
            else:
                # Jeśli mieści się w limicie -> przepuszczamy bez zmian
                final_docs.append(doc)

        return final_docs