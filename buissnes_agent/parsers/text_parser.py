import logging
import io
from typing import List, Union
from langchain_core.documents import Document
from .base_parser import BaseDocumentParser
from buissnes_agent.textchunker.source_metadata import (
    SOURCE_CHAR_END_METADATA_KEY,
    SOURCE_CHAR_START_METADATA_KEY,
    SOURCE_ENCODING_METADATA_KEY,
    SOURCE_TEXT_METADATA_KEY,
)

logger = logging.getLogger(__name__)


class TextParser(BaseDocumentParser):
    """Parser dla plików tekstowych (TXT, JSON, XML, kod), dodaje bloki kodu Markdown."""
    @staticmethod
    def _decode_text(raw_bytes: bytes) -> tuple[str, str]:
        try:
            return raw_bytes.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            return raw_bytes.decode("windows-1252"), "windows-1252"

    def parse(self, file_source: Union[str, io.BytesIO, bytes], **kwargs) -> List[Document]:
        ext = kwargs.get('ext', '')
        try:
            # Sprawdzamy czy to ścieżka do pliku, czy dane z pamięci (S3)
            if isinstance(file_source, str):
                with open(file_source, "rb") as f:
                    raw_bytes = f.read()
            elif isinstance(file_source, bytes):
                raw_bytes = file_source
            elif isinstance(file_source, io.BytesIO):
                raw_bytes = file_source.read()
            else:
                raise ValueError("Nieobsługiwany typ źródła pliku")

            content, source_encoding = self._decode_text(raw_bytes)

            if content.strip():
                ext_clean = ext.replace('.', '').lower()
                code_block_exts = {'json', 'xml', 'xsd', 'yaml', 'yml', 'js', 'py', 'java', 'html', 'csv'}

                if ext_clean in code_block_exts:
                    md_content = f"```{ext_clean}\n{content}\n```"
                else:
                    md_content = content

                metadata = {"page_number": 1}
                if md_content == content:
                    metadata.update(
                        {
                            SOURCE_TEXT_METADATA_KEY: content,
                            SOURCE_ENCODING_METADATA_KEY: source_encoding,
                            SOURCE_CHAR_START_METADATA_KEY: 0,
                            SOURCE_CHAR_END_METADATA_KEY: len(content),
                        }
                    )

                return [Document(page_content=md_content, metadata=metadata)]
            return []
        except Exception as e:
            logger.error(f"Błąd odczytu tekstu: {e}")
            return []
