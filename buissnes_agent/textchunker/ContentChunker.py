import logging
import os
import sys
import tempfile
import uuid
from typing import List, Dict, Any

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

class ContentChunker:
    """
    ### Klasa 2: Warstwa Logiki (Processing Layer)

    Odpowiada za transformację surowego tekstu w gotowe do zindeksowania wektory (dokumenty).
    Jest to "silnik" przetwarzania tekstu, niezależny od źródła danych.

    **Obsługiwane Strategie:**
    1.  **Markdown Header:** Logiczny podział wg struktury dokumentu (#, ##).
    2.  **Semantic (AI):** Podział wg znaczenia przy użyciu OpenAI Embeddings.
    3.  **Unstructured:** Zaawansowany parsing formatów (listy, tabelki).
    4.  **Recursive:** Mechaniczny podział (fallback) gwarantujący rozmiar.

    **Kluczowa funkcja: Pipeline**
    Klasa zarządza przepływem: Primary Split -> Metadata Merge -> Secondary Split (Hard Limit).
    """

    def __init__(self, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Konfiguracja Embeddingów (Inicjalizowana tylko gdy wymagana przez strategię semantic)
        # Pozwala to oszczędzić zasoby, jeśli używamy prostych strategii mechanicznych.
        self.embeddings = None
        if self.chunk_strategy == "semanticChunker":
            self.embeddings = OpenAIEmbeddings(
                model=os.getenv('EMBEDDING_MODEL'),
                base_url=os.getenv('EMBEDDING_BASE_URL'),
                api_key=os.getenv('EMBEDDING_API_KEY'),
                check_embedding_ctx_length=False
            )
        logger.info(f"ContentChunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}")

    def process_content(self, content: str, base_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        ### Główny Pipeline Przetwarzania (Orchestrator)

        To najważniejsza metoda klasy. Łączy strategię podziału z zarządzaniem limitami.

        **Etapy procesu:**
        1.  **Primary Split (Router):** Wybiera odpowiednią strategię podziału logicznego.
            Tutaj powstają chunki "merytoryczne" (np. cała sekcja rozdziału).
        2.  **Metadata Injection:** Do każdego powstałego fragmentu doklejane są metadane źródłowe (np. s3key).
        3.  **Secondary Split (Hard Limit Enforcer):** Sprawdza, czy logiczne chunki nie są za duże dla modelu LLM.
            Jeśli tak - docina je mechanicznie (metodą Recursive).
        4.  **Formatting:** Nadaje unikalne ID (_chunk_id) i zwraca czystą strukturę słownikową.
        """

        # Krok 1: Wybór strategii cięcia (Primary Split)
        splits: List[Document] = []

        if self.chunk_strategy == "markdownHeaderTextSplitter":
            splits = self._strategy_header_split(content)
        elif self.chunk_strategy == "unstructuredMarkdownLoaderSingle":
            splits = self._strategy_unstructured(content, mode="single")
        elif self.chunk_strategy == "unstructuredMarkdownLoaderElements":
            splits = self._strategy_unstructured(content, mode="elements")
        elif self.chunk_strategy == "semanticChunker":
            splits = self._strategy_semantic(content)
        elif self.chunk_strategy == "recursive":
            splits = self._strategy_recursive(content)
        else:
            # Fallback - jeśli strategia nieznana, użyj bezpiecznej rekurencji
            logger.warning(f"Unknown strategy {self.chunk_strategy}, utilizing recursive fallback.")
            splits = self._strategy_recursive(content)

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
        for doc in final_documents:
            # Generowanie unikalnego ID dla chunka (niezbędne dla baz wektorowych do upsertu/usuwania)
            if "_chunk_id" not in doc.metadata:
                doc.metadata["_chunk_id"] = str(uuid.uuid4())

            results.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })

        return results

    # --- Metody Pomocnicze i "Bezpieczniki" ---

    def _enforce_limit(self, documents: List[Document]) -> List[Document]:
        """
        ### Metoda pomocnicza: "Bezpiecznik rozmiaru" (Hard Limit Enforcer)

        **Cel:** Gwarancja techniczna.
        Strategie logiczne (Semantic, MarkdownHeader) dbają o kontekst ("nie tnij w połowie zdania"),
        ale często ignorują limit znaków ("nie tnij rozdziału, bo to jeden temat").

        Ta metoda przechodzi przez wyniki i jeśli znajdzie "giganta" (powyżej `chunk_size`),
        używa "nożyczek precyzyjnych" (RecursiveCharacterTextSplitter), aby go dociąć.

        **Ważne:** Metoda `split_documents` automatycznie kopiuje metadane rodzica do dzieci.
        """
        final_docs = []

        # Używamy Recursive jako uniwersalnej metody docinania
        recursive_cutter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]  # Hierarchia cięcia
        )

        for doc in documents:
            if len(doc.page_content) > self.chunk_size:
                # Jeśli za duży -> tniemy rekurencyjnie
                sub_docs = recursive_cutter.split_documents([doc])
                final_docs.extend(sub_docs)
            else:
                # Jeśli mieści się w limicie -> przepuszczamy bez zmian
                final_docs.append(doc)

        return final_docs

    # --- Implementacje Strategii (Engines) ---

    def _strategy_header_split(self, text: str) -> List[Document]:
        """
        ### Strategia: Markdown Headers (Strukturalna)

        Dzieli tekst w miejscach występowania nagłówków (#, ##, ###).
        Idealna dla dobrze sformatowanej dokumentacji technicznej.

        **Zaleta:** Zachowuje nagłówek w metadanych lub treści, co daje świetny kontekst.
        **Wada:** Jeśli sekcja pod nagłówkiem jest pusta lub gigantyczna, strategia sama z siebie tego nie poprawi
        (dlatego używamy _enforce_limit później).
        """
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        # strip_headers=False -> Nagłówek zostaje w tekście chunka (lepsze dla RAG)
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
        return markdown_splitter.split_text(text)

    def _strategy_recursive(self, text: str) -> List[Document]:
        """
        ### Strategia: Recursive (Mechaniczna / Fallback)

        Klasyczna metoda dzielenia tekstu. Próbuje dzielić wg hierarchii separatorów:
        1. Akapity (\n\n)
        2. Linie (\n)
        3. Zdania (.)

        Używana jako główna strategia (gdy zależy nam tylko na rozmiarze) lub jako fallback,
        gdy inne metody zawiodą.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return text_splitter.create_documents([text])

    def _strategy_unstructured(self, text: str, mode: str) -> List[Document]:
        """
        ### Strategia: Unstructured Library

        Wykorzystuje zewnętrzną bibliotekę do inteligentnego parsowania Markdown.
        Potrafi rozpoznać listy, tabelki i stopki lepiej niż zwykły regex.

        **Wymaganie:** Biblioteka `unstructured` operuje na plikach, dlatego
        musimy zapisać tekst do tymczasowego pliku (tempfile) przed przetworzeniem.

        **Modes:**
        - 'single': Cały tekst jako jeden element (z wyczyszczonym formatowaniem).
        - 'elements': Dzieli na logiczne elementy (Title, NarrativeText, ListItem).
        """
        suffix = ".md"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(text.encode("utf-8"))
            temp_file_path = temp_file.name

        try:
            loader = UnstructuredMarkdownLoader(temp_file_path, mode=mode)
            return loader.load()
        finally:
            # Sprzątanie po sobie (usuwanie pliku tymczasowego)
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _strategy_semantic(self, text: str) -> List[Document]:
        """
        ### Strategia: Semantic Chunking (Znaczeniowa)

        Najbardziej zaawansowana metoda. Nie patrzy na znaki nowej linii czy nagłówki.
        Analizuje wektory (embeddingi) zdań.

        **Jak działa:**
        1. Zamienia zdania na liczby (wektory).
        2. Oblicza podobieństwo między sąsiednimi zdaniami.
        3. Jeśli podobieństwo spada poniżej progu (breakpoint threshold), uznaje to za zmianę tematu i robi cięcie.

        **Efekt:** Chunki są bardzo spójne tematycznie, ale mogą mieć bardzo różną długość.
        """
        if not self.embeddings:
            raise ValueError("Embeddings not initialized for semantic strategy. Check env vars.")

        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,  # Wysoki próg - tnie tylko przy wyraźnej zmianie tematu
            min_chunk_size=200
        )
        return text_splitter.create_documents([text])