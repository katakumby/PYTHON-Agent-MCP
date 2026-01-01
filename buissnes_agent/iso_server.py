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

            # Logowanie sukcesu
            print(f"[RAG] Znaleziono {len(docs)} dokumentów.", file=sys.stderr)
            return "\n\n---\n\n".join([d.page_content for d in docs])

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
    # Próba załadowania ETL (ingestii danych) przy starcie
    try:
        # Import configu uruchamia ETL w tle (SearchKnowledgebase)
        # UWAGA: Config też może mieć printy, więc importujemy go ostrożnie
        import config

        print("[Server] Konfiguracja ETL załadowana.", file=sys.stderr)
    except Exception as e:
        print(f"[Server] Ostrzeżenie: Nie udało się uruchomić configu ETL: {e}", file=sys.stderr)

    print("Starting ISO20022 RAG MCP Server...", file=sys.stderr)

    # mcp.run() przejmuje stdout do komunikacji JSON.
    mcp.run()