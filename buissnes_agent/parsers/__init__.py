from .base_parser import BaseDocumentParser
from .text_parser import TextParser


def _missing_dependency_parser(class_name: str, exc: ModuleNotFoundError):
    class MissingDependencyParser(BaseDocumentParser):
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError(
                f"{class_name} requires an optional dependency that is not installed."
            ) from exc

        def parse(self, file_source, **kwargs):
            raise ModuleNotFoundError(
                f"{class_name} requires an optional dependency that is not installed."
            ) from exc

    MissingDependencyParser.__name__ = class_name
    return MissingDependencyParser


try:
    from .xlsx_parser import XlsxParser
except ModuleNotFoundError as exc:
    XlsxParser = _missing_dependency_parser("XlsxParser", exc)

try:
    from .docx_parser import DocxParser
except ModuleNotFoundError as exc:
    DocxParser = _missing_dependency_parser("DocxParser", exc)

try:
    from .pdf_parser import PdfParser
except ModuleNotFoundError as exc:
    PdfParser = _missing_dependency_parser("PdfParser", exc)

try:
    from .pptx_parser import PptxParser
except ModuleNotFoundError as exc:
    PptxParser = _missing_dependency_parser("PptxParser", exc)


__all__ = [
    "BaseDocumentParser",
    "XlsxParser",
    "DocxParser",
    "PdfParser",
    "TextParser",
    "PptxParser",
]
