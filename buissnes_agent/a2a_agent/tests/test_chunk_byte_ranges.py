import unittest
from types import SimpleNamespace

from buissnes_agent.parsers import TextParser
from buissnes_agent.textchunker.langchain.LangChainChunker import LangChainChunker
from buissnes_agent.tools.tool_iso_rag import _format_search_results


class MarkdownChunkByteRangeTests(unittest.TestCase):
    def test_markdown_chunks_store_byte_ranges_from_original_file(self) -> None:
        original_text = (
            "# Intro\n\n"
            "Zażółć gęślą jaźń. " * 8
            + "\n\n## Details\n"
            + "Second section keeps enough text to trigger recursive splitting.\n" * 4
        )
        parser = TextParser()
        documents = parser.parse(original_text.encode("utf-8"), ext=".md")

        chunker = LangChainChunker(
            "markdownHeaderTextSplitter",
            chunk_size=80,
            chunk_overlap=15,
        )
        results = chunker.process_content(documents)

        self.assertGreater(len(results), 2)

        original_bytes = original_text.encode("utf-8")
        for item in results:
            metadata = item["metadata"]
            self.assertIn("start_byte", metadata)
            self.assertIn("end_byte", metadata)
            chunk_bytes = original_bytes[
                metadata["start_byte"] : metadata["end_byte"] + 1
            ]
            self.assertEqual(chunk_bytes.decode("utf-8"), item["text"])

    def test_wrapped_code_chunks_do_not_claim_exact_byte_ranges(self) -> None:
        parser = TextParser()
        documents = parser.parse(b'{"hello":"world"}', ext=".json")

        chunker = LangChainChunker(
            "recursive",
            chunk_size=50,
            chunk_overlap=0,
        )
        results = chunker.process_content(documents)

        self.assertEqual(len(results), 1)
        self.assertNotIn("start_byte", results[0]["metadata"])
        self.assertNotIn("end_byte", results[0]["metadata"])


class RagFormattingByteRangeTests(unittest.TestCase):
    def test_format_search_results_includes_byte_range(self) -> None:
        point = SimpleNamespace(
            payload={
                "phrase": "# Header\n\nExample chunk",
                "title": "file.md",
                "source": "s3://agent-documents/business/file.md",
                "url": "https://agent-documents.s3.amazonaws.com/business/file.md",
                "domain": "business",
                "extension": ".md",
                "phrase_metadata_id": "chunk-1",
                "start_byte": 12,
                "end_byte": 42,
            },
            score=0.98,
        )

        formatted = _format_search_results([point])

        self.assertIn("Zakres bajtów: bytes=12-42", formatted)
