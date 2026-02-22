import logging
from typing import Generator

import boto3

from buissnes_agent.config_loader import settings

logger = logging.getLogger(__name__)

class DataLoaderS3Service:
    def __init__(self):
        # Konfiguracja AWS / MinIO
        self.aws_key = settings.get("data_source.s3.access_key")
        self.aws_secret = settings.get("data_source.s3.secret_key")
        self.aws_region = settings.get("data_source.s3.region", "us-east-1")
        self.s3_endpoint = settings.get("data_source.s3.endpoint")

        if not self.aws_key or not self.aws_secret:
            raise RuntimeError("Brak poświadczeń AWS w pliku .env (S3_AKID, S3_SK).")

        self.session = boto3.Session(
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret,
            region_name=self.aws_region,
        )

        # Wybór klienta (MinIO vs AWS)
        if self.s3_endpoint:
            self.s3_client = self.session.client('s3', endpoint_url=self.s3_endpoint)
            logger.info(f"S3Service: Połączono z S3 (Local/Custom): {self.s3_endpoint}")
        else:
            self.s3_client = self.session.client('s3')
            logger.info("S3Service: Połączono z AWS S3")

    def list_objects(self, bucket_name: str, prefix: str = "") -> Generator[str, None, None]:
        """
        Generator zwracający klucze plików z S3 pasujące do rozszerzeń
        """
        paginator = self.s3_client.get_paginator('list_objects_v2')
        prefix_arg = prefix if prefix else ""

        allowed_exts = settings.get("chunking.allowed_extensions", [])
        ext_tuple = tuple(allowed_exts)

        try:
            for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix_arg):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        # Filtrowanie obsługiwanych formatów tekstowych
                        if key.endswith(ext_tuple):
                            yield key
        except Exception as e:
            logger.error(f"S3Service Error listing objects: {e}")
            raise e

    def download_text(self, bucket_name: str, object_key: str) -> str:
        """
        Pobiera treść pliku i dekoduje ją do stringa
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            data = response["Body"].read()
            try:
                return data.decode("utf-8")
            except UnicodeDecodeError:
                return data.decode("windows-1252")
        except Exception as e:
            logger.error(f"S3Service Error downloading {object_key}: {e}")
            raise e

    def download_bytes(self, bucket_name: str, key: str) -> bytes:
        """Pobiera obiekt z S3 jako surowe bajty (dla PDF/Obrazów)."""
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            return response['Body'].read()
        except Exception as e:
            print(f"S3 Download Error (Bytes): {e}")
            raise e