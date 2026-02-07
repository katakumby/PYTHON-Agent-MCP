import logging
from typing import Dict, Any, Generator, Tuple

from s3_service import S3Service

logger = logging.getLogger(__name__)


class S3FileLoader:
    """
    Klasa odpowiedzialna za Warstwę Danych: Deleguje pobieranie plików do klasy `S3Service`
    oraz przygotowuje wstępne metadane na podstawie ścieżki pliku.
    """

    def __init__(self, bucket_name: str, prefix: str):
        self.bucket_name = bucket_name
        self.prefix = prefix

        # Inicjalizacja serwisu S3 (delegacja połączenia)
        self.s3_service = S3Service()
        logger.info(f"S3FileLoader initialized. Bucket: {bucket_name}")

    def list_objects(self) -> Generator[str, None, None]:
        """Wrapper na metodę z serwisu S3 - zwraca listę plików do przetworzenia."""
        return self.s3_service.list_objects(self.bucket_name, self.prefix)

    def load_file_with_metadata(self, s3_key: str) -> Tuple[str, Dict[str, Any]]:
        """
        Pobiera treść pliku i generuje metadane źródłowe.

        Realizuje część oryginalnego procesu:
        1. Pobranie: Ściąga treść pliku z S3 do pamięci RAM.
        2. Metadata: Przygotowuje informacje o źródle (s3key, domena).
        """

        # 1. Pobranie treści
        content = self.s3_service.download_text(self.bucket_name, s3_key)

        # 2. Logika wyciągania metadanych
        metadata = {
            "source_file": s3_key,
            "s3key": s3_key
        }

        # 3. Dodanie Metadanych (Source file info)
        # Usuwamy prefix, żeby dostać czystą ścieżkę względną dla domeny
        key_without_prefix = s3_key
        if self.prefix and s3_key.startswith(self.prefix):
            key_without_prefix = s3_key[len(self.prefix):].lstrip("/")

        # Wyciąganie "domeny" biznesowej (pierwszy katalog w ścieżce)
        domain_name = key_without_prefix.split('/')[0] if '/' in key_without_prefix else None

        if domain_name:
            metadata["domain"] = domain_name

        return content, metadata