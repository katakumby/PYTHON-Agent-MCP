from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

# Import interfejsu bazowego (zakładając strukturę katalogów)
from buissnes_agent.textchunker.langchain.base import ChunkingStrategy


class MarkdownHeaderStrategy(ChunkingStrategy):
    """
    ### Strategia 1: Markdown Headers (Strukturalna)

    Dzieli tekst w miejscach występowania nagłówków (#, ##, ###).
    Idealna dla dobrze sformatowanej dokumentacji technicznej.

    **Zaleta:** Zachowuje nagłówek w metadanych lub treści, co daje świetny kontekst.
    **Wada:** Jeśli sekcja pod nagłówkiem jest pusta lub gigantyczna, strategia sama z siebie tego nie poprawi.

    **Implementacja:**
    Logika została wyizolowana. Klasa nie potrzebuje zewnętrznych parametrów (chunk_size),
    ponieważ tnie strictly po strukturze dokumentu.
    """

    def split_text(self, text: str) -> List[Document]:
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        # strip_headers=False -> Nagłówek zostaje w tekście chunka (lepsze dla RAG)
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )
        return markdown_splitter.split_text(text)