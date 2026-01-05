import os
import logging
import boto3
import tempfile
import uuid
from typing import List, Dict, Any, Generator

# Importy z Twojego kodu
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class S3Chunker:
    def __init__(self, bucket_name: str, prefix: str, chunk_strategy: str, chunk_size: int, chunk_overlap: int):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Konfiguracja AWS / MinIO
        self.aws_key = os.getenv('S3_AKID') or os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret = os.getenv('S3_SK') or os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION') or os.getenv('S3_REGION') or "eu-north-1"
        self.s3_endpoint = os.getenv('S3_ENDPOINT')  # <--- NOWA ZMIENNA DLA MINIO

        if not self.aws_key or not self.aws_secret:
            raise RuntimeError("Brak poświadczeń AWS w pliku .env (S3_AKID, S3_SK).")

        self.session = boto3.Session(
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret,
            region_name=self.aws_region,
        )

        # Jeśli podano endpoint (MinIO), używamy go. Jeśli nie (AWS), boto3 użyje domyślnego.
        if self.s3_endpoint:
            self.s3_client = self.session.client('s3', endpoint_url=self.s3_endpoint)
            logger.info(f"Połączono z S3 (Local/Custom): {self.s3_endpoint}")
        else:
            self.s3_client = self.session.client('s3')
            logger.info("Połączono z AWS S3")

        # Embeddings... (reszta bez zmian)
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('EMBEDDING_MODEL'),
            base_url=os.getenv('EMBEDDING_BASE_URL'),
            api_key=os.getenv('EMBEDDING_API_KEY'),
            check_embedding_ctx_length=False
        )

    def list_objects(self) -> Generator[str, None, None]:
        """Generator zwracający klucze plików z S3"""
        paginator = self.s3_client.get_paginator('list_objects_v2')

        # Jeśli prefix jest pusty, szukamy w całym buckecie
        prefix_arg = self.prefix if self.prefix else ""

        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix_arg):
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Filtrowanie rozszerzeń - dodaj te, które chcesz obsługiwać
                    # Uwaga: Twoje strategie chunkingu muszą umieć obsłużyć te formaty!
                    if key.endswith(('.md', '.txt', '.xml', '.xsd', '.json')):
                        yield key

    def _download_s3_object_to_variable(self, object_key: str) -> str:
        """Pobiera treść pliku z S3 do pamięci"""
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
        data = response["Body"].read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("windows-1252")

    def process_file(self, s3_key: str) -> List[Dict[str, Any]]:
        """
        Pobiera plik, tnie go wg strategii i zwraca listę słowników z tekstem i metadanymi.
        Zwraca format: [{'text': str, 'metadata': dict}, ...]
        """
        content = self._download_s3_object_to_variable(s3_key)

        # 1. Primary Split (Strategie z Twojego kodu)
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

        # 2. Add Metadata (Source file info)
        key_without_prefix = s3_key.replace(self.prefix, "").lstrip("/")
        domain_name = key_without_prefix.split('/')[0] if '/' in key_without_prefix else None

        for doc in splits:
            doc.metadata["source_file"] = s3_key
            doc.metadata["s3key"] = s3_key
            if domain_name:
                doc.metadata["domain"] = domain_name

        # 3. Secondary Split (Recursive / MarkdownTextSplitter) jeśli chunk_size > 0
        final_documents = splits
        if self.chunk_size > 0:
            # Dodanie chunk_id przed podziałem
            for doc in splits:
                doc.metadata["_chunk_id"] = str(uuid.uuid4())

            # W Twoim kodzie było zakomentowane Recursive, ale prosiłeś o dodanie.
            # Używamy MarkdownTextSplitter jako domyślnego dla markdownów,
            # ale tu jest opcja użycia RecursiveCharacterTextSplitter.

            # text_splitter = RecursiveCharacterTextSplitter(
            #    chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, separators=["\n\n", "\n", ".", " ", ""]
            # )
            text_splitter = MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

            final_documents = text_splitter.split_documents(splits)

        # 4. Konwersja na prosty format dla SearchKnowledgebase
        results = []
        for doc in final_documents:
            results.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })

        return results

    # --- Implementacje Strategii ---

    def _strategy_header_split(self, text: str):
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        return markdown_splitter.split_text(text)

    def _strategy_unstructured(self, text: str, mode: str):
        # Unstructured wymaga pliku, tworzymy temp
        suffix = ".md"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(text.encode("utf-8"))
            temp_file_path = temp_file.name

        try:
            loader = UnstructuredMarkdownLoader(temp_file_path, mode=mode)
            return loader.load()
        finally:
            os.remove(temp_file_path)

    def _strategy_semantic(self, text: str):
        text_splitter = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
            min_chunk_size=200
        )
        return text_splitter.create_documents([text])