from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import ExperimentalMarkdownSyntaxTextSplitter

# Import interfejsu bazowego (zakładając strukturę katalogów)
from buissnes_agent.textchunker.langchain.base import ChunkingStrategy
from buissnes_agent.textchunker.source_metadata import (
    SOURCE_CHAR_END_METADATA_KEY,
    SOURCE_CHAR_START_METADATA_KEY,
    SOURCE_TEXT_METADATA_KEY,
)


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

    def split_documents(self, documents: List[Document]) -> List[Document]:
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = ExperimentalMarkdownSyntaxTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )

        final_chunks = []
        for doc in documents:
            # Dzielimy treść pojedynczej strony (doc)
            chunks = markdown_splitter.split_text(doc.page_content)
            search_from = 0

            # Ręcznie dodajemy metadane strony do nowych chunków
            for chunk in chunks:
                merged_metadata = doc.metadata.copy()
                merged_metadata.update(chunk.metadata)

                source_text = doc.metadata.get(SOURCE_TEXT_METADATA_KEY)
                parent_char_start = doc.metadata.get(SOURCE_CHAR_START_METADATA_KEY)
                if isinstance(source_text, str) and isinstance(parent_char_start, int):
                    local_start = doc.page_content.find(chunk.page_content, search_from)
                    if local_start >= 0:
                        chunk_char_start = parent_char_start + local_start
                        merged_metadata[SOURCE_CHAR_START_METADATA_KEY] = chunk_char_start
                        merged_metadata[SOURCE_CHAR_END_METADATA_KEY] = (
                            chunk_char_start + len(chunk.page_content)
                        )
                        search_from = local_start + len(chunk.page_content)
                    else:
                        merged_metadata.pop(SOURCE_CHAR_START_METADATA_KEY, None)
                        merged_metadata.pop(SOURCE_CHAR_END_METADATA_KEY, None)

                final_chunks.append(
                    Document(
                        page_content=chunk.page_content,
                        metadata=merged_metadata,
                    )
                )

        return final_chunks
