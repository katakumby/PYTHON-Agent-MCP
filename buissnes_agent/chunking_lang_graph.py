import logging
import os
import sys
from typing import List

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


# Opakowuje funkcje w klasę, aby SearchKnowledgebase mógł ich używać dynamicznie.
class AdvancedChunker:
    """
    Klasa odpowiedzialna za zaawansowany podział tekstu (Chunking) przy użyciu bibliotek LangChain.
    Obsługuje strategie:
    1. Markdown Header (strukturalna)
    2. Semantic (znaczeniowa - AI)
    3. Recursive (mechaniczna - fallback)
    """

    def __init__(self, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Konfiguracja Embeddingów z .env dla SemanticChunker
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('EMBEDDING_BASE_URL'),
            api_key=os.getenv('EMBEDDING_API_KEY'),
            check_embedding_ctx_length=False
        )
        logger.info(f"AdvancedChunker initialized. Strategy: {chunk_strategy}, Max Chunk Size: {chunk_size}")

    def split_text(self, text: str) -> List[str]:
        """
        ### Router strategii (Dispatcher)

        Wybiera metodę cięcia na podstawie konfiguracji .env.
        Jest to główny punkt wejścia dla klasy SearchKnowledgebase.
        """
        if not text:
            return []

        if self.chunk_strategy == "markdown_header":
            return self.markdownHeaderTextSplitter(text)
        elif self.chunk_strategy == "semantic":
            return self.semanticChunker(text)
        elif self.chunk_strategy == "recursive":
            return self.recursiveSplitter(text)
        else:
            logger.warning(f"Unknown strategy {self.chunk_strategy}, using fallback.")
            return self.recursiveSplitter(text)

    def _enforce_limit(self, chunks: List[str]) -> List[str]:
        """
        ### Metoda pomocnicza: "Bezpiecznik rozmiaru" (Hard Limit Enforcer)

        **Co robi:**
        Przechodzi przez listę otrzymanych chunków. Jeśli którykolwiek przekracza
        zdefiniowany `chunk_size`, dzieli go na mniejsze kawałki używając metody Recursive.

        **Dlaczego jest potrzebna:**
        Metody takie jak SemanticChunker czy MarkdownSplitter dzielą tekst logicznie
        (wg znaczenia lub nagłówków), często ignorując limit znaków.
        Może to prowadzić do powstania chunków o wielkości np. 5000 znaków,
        które "zapchają" okno kontekstowe LLM-a.
        Ta metoda gwarantuje, że wynik końcowy zawsze zmieści się w limicie `chunk_size`.
        """
        if self.chunk_size <= 0:
            return chunks

        final_chunks = []
        # Używamy Recursive jako "nożyczek precyzyjnych" dla zbyt dużych fragmentów
        recursive_cutter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        for chunk in chunks:
            # Sprawdzenie warunku długości
            if len(chunk) > self.chunk_size:
                # Jeśli za duży -> potnij go na mniejsze pod-chunki
                sub_chunks = recursive_cutter.split_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                # Jeśli mieści się w limicie -> zostaw bez zmian
                final_chunks.append(chunk)

        return final_chunks

    def markdownHeaderTextSplitter(self, text: str, headers_to_split_on=None):
        """
        ### Strategia: Podział wg struktury dokumentu (Markdown)

        **Działanie:**
        1. Dzieli tekst w miejscach występowania nagłówków (#, ##, ###).
        2. Uruchamia `_enforce_limit`, aby pociąć zbyt długie sekcje pod nagłówkami.

        **Zastosowanie:**
        Idealne dla dokumentacji technicznej, gdzie każdy nagłówek to osobny temat.
        """
        if headers_to_split_on is None:
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

        # Krok 1: Logiczny podział wg nagłówków
        # strip_headers=False zachowuje nagłówek w treści chunka (ważne dla kontekstu)
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
        md_header_splits = markdown_splitter.split_text(text)

        # Wyciągamy sam tekst z obiektów Document
        content_splits = [doc.page_content for doc in md_header_splits]

        # Krok 2: Docinanie techniczne (Hard limit)
        if self.chunk_size > 0:
            return self._enforce_limit(content_splits)

        return content_splits

    def semanticChunker(self, text: str):
        """
        ### Strategia: Podział semantyczny (wg znaczenia)

        **Działanie:**
        1. Używa modelu embeddingów (OpenAI/Nomic) do analizy zdań.
        2. Grupuje zdania, które są blisko siebie tematycznie (podobieństwo cosinusowe).
        3. Przekazuje wynik do `_enforce_limit`.

        **Dlaczego Hybrid Approach:**
        SemanticChunker jest najlepszy do RAG, bo nie ucina wątku w połowie.
        Jednak jeśli tekst jest bardzo spójny (np. 10 stron prawniczego bełkotu),
        SemanticChunker może zwrócić jeden gigantyczny blok.
        Dlatego na końcu musimy użyć `_enforce_limit`, aby pociąć go mechanicznie,
        jeśli przekroczył dozwolony rozmiar.
        """
        # Krok 1: Cięcie semantyczne (duże bloki znaczeniowe)
        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            # Próg 90.0 oznacza, że łączymy zdania, dopóki nagła zmiana tematu nie nastąpi.
            breakpoint_threshold_amount=90.0,
            min_chunk_size=100
        )
        docs = text_splitter.create_documents([text])
        semantic_chunks = [doc.page_content for doc in docs]

        # Krok 2: Wymuszenie limitu znaków (Hard limit)
        # Kluczowe dla naprawienia problemu "za dużych chunków"
        final_chunks = self._enforce_limit(semantic_chunks)

        return final_chunks

    def recursiveSplitter(self, text: str):
        """
        ### Strategia: Podział rekurencyjny (Fallback)

        **Działanie:**
        Próbuje dzielić tekst wg hierarchii separatorów, aż chunk zmieści się w limicie:
        1. Podwójna nowa linia (\n\n) - akapity
        2. Pojedyncza nowa linia (\n)
        3. Kropka (.) - zdania
        4. Spacja

        **Zastosowanie:**
        Metoda zapasowa. Gwarantuje idealny rozmiar chunków i overlap,
        ale nie "rozumie" tekstu, więc może przeciąć wątek w nieodpowiednim momencie.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return text_splitter.split_text(text)