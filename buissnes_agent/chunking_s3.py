import logging
import os
import tempfile
import uuid
from typing import List, Dict, Any, Generator

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from s3_service import S3Service

logger = logging.getLogger(__name__)


class S3Chunker:
    """
    Klasa odpowiedzialna za pobieranie plików z chmury (S3/MinIO) i ich podział (Chunking).

    Łączy w sobie dwie odpowiedzialności:
    1. Warstwa Danych: Deleguje pobieranie plików do klasy `S3Service`.
    2. Warstwa Logiki: Dzieli pobraną treść wybraną strategią (Markdown, Semantic, Unstructured).
    """

    def __init__(self, bucket_name: str, prefix: str, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Inicjalizacja serwisu S3 (delegacja połączenia)
        self.s3_service = S3Service()

        # Konfiguracja Embeddingów (wymagana tylko dla strategii Semantic)
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('EMBEDDING_BASE_URL'),
            api_key=os.getenv('EMBEDDING_API_KEY'),
            check_embedding_ctx_length=False
        )
        logger.info(f"S3Chunker initialized. Strategy: {chunk_strategy}")

    def list_objects(self) -> Generator[str, None, None]:
        """Wrapper na metodę z serwisu S3 - zwraca listę plików do przetworzenia."""
        return self.s3_service.list_objects(self.bucket_name, self.prefix)

    def process_file(self, s3_key: str) -> List[Dict[str, Any]]:
        """
        ### Główna metoda orkiestracji (Pipeline)

        **Przepływ działania:**
        1. **Pobranie:** Ściąga treść pliku z S3 do pamięci RAM.
        2. **Primary Split:** Dzieli tekst logicznie wg wybranej strategii (np. po nagłówkach lub semantycznie).
        3. **Metadata:** Dodaje informacje o źródle (s3key, domena).
        4. **Secondary Split (Hard Limit):** Docina fragmenty, które są nadal za duże (powyżej `chunk_size`).
        5. **Formatowanie:** Zwraca listę gotową do zapisu w Qdrant.
        """
        # 1. Pobranie treści
        content = self.s3_service.download_text(self.bucket_name, s3_key)

        # 2. Wybór strategii cięcia (Primary Split)
        splits = []
        if self.chunk_strategy == "markdownHeaderTextSplitter":
            splits = self._strategy_header_split(content)
        elif self.chunk_strategy == "unstructuredMarkdownLoaderSingle":
            splits = self._strategy_unstructured(content, mode="single")
        elif self.chunk_strategy == "unstructuredMarkdownLoaderElements":
            splits = self._strategy_unstructured(content, mode="elements")
        elif self.chunk_strategy == "semanticChunker":
            splits = self._strategy_semantic(content)
        else:
            # Fallback
            splits = self._strategy_header_split(content)

        # 3. Dodanie Metadanych (Source file info)
        # Usuwamy prefix, żeby dostać czystą ścieżkę względną dla domeny
        key_without_prefix = s3_key
        if self.prefix and s3_key.startswith(self.prefix):
            key_without_prefix = s3_key[len(self.prefix):].lstrip("/")

        # Wyciąganie "domeny" biznesowej (pierwszy katalog w ścieżce)
        domain_name = key_without_prefix.split('/')[0] if '/' in key_without_prefix else None

        for doc in splits:
            doc.metadata["source_file"] = s3_key
            doc.metadata["s3key"] = s3_key
            if domain_name:
                doc.metadata["domain"] = domain_name

        # 4. Secondary Split (Jeśli zdefiniowano chunk_size)
        # To jest "Bezpiecznik". Strategie logiczne (np. HeaderSplitter) mogą zwrócić
        # chunk o długości 5000 znaków. Tutaj docinamy go mechanicznie do limitu (np. 600).
        final_documents = splits
        if self.chunk_size > 0:
            for doc in splits:
                doc.metadata["_chunk_id"] = str(uuid.uuid4())

            # Używamy MarkdownTextSplitter do docinania (stara się nie ciąć w środku słowa/znacznika)
            text_splitter = MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            final_documents = text_splitter.split_documents(splits)

        # 5. Formatowanie wyniku dla SearchKnowledgebase
        results = []
        for doc in final_documents:
            results.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })

        return results

    # --- Strategie Chunkingu ---

    def _strategy_header_split(self, text: str):
        """
        Strategia: Markdown Headers

        Dzieli tekst w oparciu o strukturę nagłówków (#, ##, ###).
        Idealne do dokumentacji, gdzie kontekst jest zawarty w sekcjach.
        """
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        return markdown_splitter.split_text(text)

    def _strategy_unstructured(self, text: str, mode: str):
        """
        Strategia: Unstructured Library

        Wykorzystuje potężną bibliotekę 'unstructured' do parsowania Markdown.
        Wymaga zapisania treści do pliku tymczasowego, ponieważ biblioteka operuje na plikach.

        Modes:
        - 'single': Zwraca cały dokument jako jeden element (potem cięty w Secondary Split).
        - 'elements': Dzieli dokument na akapity, listy itp.
        """
        suffix = ".md"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(text.encode("utf-8"))
            temp_file_path = temp_file.name

        try:
            loader = UnstructuredMarkdownLoader(temp_file_path, mode=mode)
            return loader.load()
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _strategy_semantic(self, text: str):
        """
        Strategia: Semantic Chunking

        Dzieli tekst na podstawie znaczenia (embeddingów).
        Grupuje zdania tematycznie, aż nastąpi duża zmiana tematu (breakpoint).
        Zwraca zazwyczaj bardzo spójne merytorycznie fragmenty.
        """
        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
            min_chunk_size=200
        )
        return text_splitter.create_documents([text])