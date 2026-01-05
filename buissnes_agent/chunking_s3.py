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
    def __init__(self, bucket_name: str, prefix: str, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Inicjalizacja serwisu S3 (delegacja połączenia)
        self.s3_service = S3Service()

        # Konfiguracja Embeddingów (dla Semantic Chunker)
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('EMBEDDING_BASE_URL'),
            api_key=os.getenv('EMBEDDING_API_KEY'),
            check_embedding_ctx_length=False
        )
        logger.info(f"S3Chunker initialized. Strategy: {chunk_strategy}")

    def list_objects(self) -> Generator[str, None, None]:
        """Wrapper na metodę z serwisu S3"""
        return self.s3_service.list_objects(self.bucket_name, self.prefix)

    def process_file(self, s3_key: str) -> List[Dict[str, Any]]:
        """
        Pobiera plik (przez S3Service), tnie go wg strategii i zwraca listę słowników.
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
        # Usuwamy prefix, żeby dostać czystą ścieżkę względną
        key_without_prefix = s3_key
        if self.prefix and s3_key.startswith(self.prefix):
            key_without_prefix = s3_key[len(self.prefix):].lstrip("/")

        domain_name = key_without_prefix.split('/')[0] if '/' in key_without_prefix else None

        for doc in splits:
            doc.metadata["source_file"] = s3_key
            doc.metadata["s3key"] = s3_key
            if domain_name:
                doc.metadata["domain"] = domain_name

        # 4. Secondary Split (Jeśli zdefiniowano chunk_size)
        final_documents = splits
        if self.chunk_size > 0:
            for doc in splits:
                doc.metadata["_chunk_id"] = str(uuid.uuid4())

            # Tu zmienić na RecursiveCharacterTextSplitter jeśli potrzeba
            # text_splitter = RecursiveCharacterTextSplitter(
            #    chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, separators=["\n\n", "\n", ".", " ", ""]
            # )
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
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        return markdown_splitter.split_text(text)

    def _strategy_unstructured(self, text: str, mode: str):
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
        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
            min_chunk_size=200
        )
        return text_splitter.create_documents([text])