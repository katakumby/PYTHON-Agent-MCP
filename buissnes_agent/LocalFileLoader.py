import logging
import os
import sys
from typing import Generator, Tuple, Dict, Any

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# --- Helper Class dla plików lokalnych ---
# Tworzymy to, aby ujednolicić interfejs. Teraz Local i S3 działają tak samo:
# mają metodę list_objects() i load_file().
class LocalFileLoader:
    """
    Pomocnicza klasa adaptera dla plików lokalnych.
    Sprawia, że pliki z dysku wyglądają dla systemu tak samo jak pliki z S3.
    """

    def __init__(self, directory: str):
        self.directory = os.path.abspath(directory)

    def list_objects(self) -> Generator[str, None, None]:
        """Generator zwracający ścieżki do plików."""
        if not os.path.exists(self.directory):
            logger.error(f"Katalog nie istnieje: {self.directory}")
            return

        for root, _, files in os.walk(self.directory):
            for file in files:
                # Filtracja rozszerzeń
                ext = os.path.splitext(file)[1].lower()
                if ext in [".md", ".txt", ".xml", ".xsd"]:
                    yield os.path.join(root, file)

    def load_file_with_metadata(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """Zwraca treść i metadane pliku lokalnego."""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Metadane dla pliku lokalnego
            metadata = {
                "source_file": os.path.basename(file_path),
                "filepath": file_path
            }
            return content, metadata
        except Exception as e:
            logger.error(f"Błąd odczytu {file_path}: {e}")
            return "", {}
