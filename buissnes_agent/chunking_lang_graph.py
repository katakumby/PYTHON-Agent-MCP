import os
import logging
import sys
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


# Opakowuje funkcje w klasę, aby SearchKnowledgebase mógł ich używać dynamicznie.
class AdvancedChunker:
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
        logger.info(f"AdvancedChunker initialized. Strategy: {chunk_strategy}")

    def split_text(self, text: str) -> List[str]:
        """
        ### Router strategii
        Wybiera metodę cięcia na podstawie konfiguracji .env.
        """
        if self.chunk_strategy == "markdown_header":
            return self.markdownHeaderTextSplitter(text)
        elif self.chunk_strategy == "semantic":
            return self.semanticChunker(text)
        elif self.chunk_strategy == "recursive":
            return self.recursiveSplitter(text)
        else:
            logger.warning(f"Unknown strategy {self.chunk_strategy}, using fallback.")
            return self.recursiveSplitter(text)

    def markdownHeaderTextSplitter(self, text: str, headers_to_split_on=None):
        """
        Dzieli tekst na podstawie nagłówków Markdown (#, ##, ###).
        """
        if headers_to_split_on is None:
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

        # markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(text)

        # Obsługa parametru chunk_size wewnątrz nagłówków
        if self.chunk_size > 0:
            text_splitter = MarkdownTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            final_documents = text_splitter.split_documents(md_header_splits)
            # Zwracamy czysty tekst
            return [doc.page_content for doc in final_documents]

        return [doc.page_content for doc in md_header_splits]

    def semanticChunker(self, text: str):
        """
        Używa SemanticChunker z breakpoint_threshold_type="percentile".
        """
        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
            min_chunk_size=200
        )
        docs = text_splitter.create_documents([text])
        return [doc.page_content for doc in docs]

    def recursiveSplitter(self, text: str):
        """
        adaptacja RecursiveCharacterTextSplitter)
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return text_splitter.split_text(text)