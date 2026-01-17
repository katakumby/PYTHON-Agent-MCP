import asyncio
import logging
import os
import sys

import qdrant_client
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Wyciszamy logi bibliotek, które mogą śmiecić na stdout
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

load_dotenv()

# Inicjalizacja MCP
mcp = FastMCP("ISO20022 RAG Service")

# 2. Konfiguracja Klientów
try:
    emb_model = os.getenv('EMBEDDING_MODEL')
    emb_url = os.getenv('EMBEDDING_BASE_URL')
    emb_key = os.getenv('EMBEDDING_API_KEY')

    if not emb_model:
        raise ValueError("Brak zmiennej EMBEDDING_MODEL w pliku .env")

    # Inicjalizacja Qdrant
    qdrant_client_instance = qdrant_client.QdrantClient(
        url=os.getenv('QDRANT_API'),
        api_key=os.getenv('QDRANT_API_KEY'),
    )

    # Inicjalizacja Embeddingów
    embeddings = OpenAIEmbeddings(
        model=emb_model,
        base_url=emb_url,
        api_key=emb_key,
        check_embedding_ctx_length=False
    )
    # ZMIANA: print na stderr
    print(f"[Server] Połączono z Qdrant i skonfigurowano Embeddingi: {emb_model}", file=sys.stderr)

except Exception as e:
    # ZMIANA: print na stderr
    print(f"[Server] Błąd inicjalizacji klientów: {e}", file=sys.stderr)
    qdrant_client_instance = None
    embeddings = None


# 3. Helper do RAG
def get_qdrant_retriever(collection_name: str, top_k: int):
    if not qdrant_client_instance or not embeddings:
        raise RuntimeError("Klient Qdrant lub Embeddings nie zostały zainicjalizowane.")

    vector_store = QdrantVectorStore(
        client=qdrant_client_instance,
        collection_name=collection_name,
        embedding=embeddings
    )
    return vector_store.as_retriever(search_kwargs={"k": top_k})


# ==============================================================================
# NARZĘDZIA MCP (TOOLS)
# ==============================================================================

@mcp.tool()
async def query_iso20022_knowledge_base(query: str) -> str:
    """
    Wyszukuje i zwraca informacje dotyczące wpływu zmian biznesowych związanych z ISO 20022 / CBPR+
    oraz ogólną dokumentację standardu ISO 20022.

    Argumenty:
        query: Pytanie lub temat do wyszukania w bazie wektorowej.
    """
    collection_name = os.getenv("COLLECTION_NAME")
    top_k = 5

    print(f"[RAG] Szukam: '{query}' w kolekcji '{collection_name}'", file=sys.stderr)

    try:
        def _sync_search():
            retriever = get_qdrant_retriever(collection_name, top_k)
            docs = retriever.invoke(query)

            if not docs:
                return "No relevant documents found."

            # FORMATOWANIE ODPOWIEDZI Z METADANYMI
            formatted_results = []
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source_file", "unknown")
                # Doklejamy nagłówek źródła do treści, którą widzi LLM
                formatted_results.append(f"--- DOCUMENT {i} (Source: {source}) ---\n{doc.page_content}")

            return "\n\n".join(formatted_results)

        result = await asyncio.to_thread(_sync_search)
        return result

    except Exception as e:
        err_msg = f"Error querying knowledge base: {str(e)}"
        print(f"[RAG Error] {err_msg}", file=sys.stderr)
        return err_msg


# ==============================================================================
# URUCHOMIENIE
# ==============================================================================

if __name__ == "__main__":
    import argparse

    # Próba załadowania ETL
    try:
        import config

        print("[Server] Konfiguracja ETL załadowana.", file=sys.stderr)
    except Exception as e:
        print(f"[Server] Warning: ETL config error: {e}", file=sys.stderr)

    # Obsługa argumentów (referencja A2A)
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--host", default="0.0.0.0")

    # FastMCP przejmuje sys.argv.
    # jawnie kontrolowanie trybu SSE
    # Prostsze podejście zgodne z FastMCP:
    # FastMCP automatycznie wykrywa, czy ma działać jako stdio czy server,

    print("Starting ISO20022 RAG MCP Server...", file=sys.stderr)

    # Aby umożliwić działanie jako serwer HTTP (SSE) dla "prawdziwego" A2A:
    # Uruchomienie: python iso_server.py --transport sse --port 8000

    # Pobieramy argumenty "ręcznie" tylko po to by zdecydować o metodzie run
    if "--transport" in sys.argv and "sse" in sys.argv:
        mcp.run(transport="sse")  # FastMCP nasłuchuje na porcie domyślnym lub z env
    else:
        mcp.run(transport="stdio")