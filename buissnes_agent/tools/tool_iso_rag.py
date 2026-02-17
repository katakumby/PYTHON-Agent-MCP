import os
import sys
import logging
import qdrant_client
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

# ==============================================================================
# ZASOBY GLOBALNE (SINGLETONY)
# ==============================================================================
# Przechowujemy instancje klienta Qdrant i modelu Embeddingów globalnie,
# aby nie tworzyć nowego połączenia przy każdym zapytaniu (optymalizacja).
_qdrant_client = None
_embeddings = None


def _init_resources():
    """
    ### LENIWA INICJALIZACJA ZASOBÓW (Lazy Loading)

    Ta funkcja jest wywoływana dopiero przy pierwszym użyciu narzędzia.

    Dlaczego:
    1. Szybszy start serwera (nie czekamy na połączenie z bazą przy bootowaniu).
    2. Odporność na błędy (jeśli Qdrant leży, serwer wstanie, a błąd pojawi się dopiero przy pytaniu).
    """
    global _qdrant_client, _embeddings

    # Jeśli zasoby już istnieją, nie rób nic.
    if _qdrant_client and _embeddings:
        return

    try:
        # Pobranie konfiguracji z .env
        emb_model = os.getenv('EMBEDDING_MODEL')
        emb_url = os.getenv('EMBEDDING_BASE_URL')
        emb_key = os.getenv('EMBEDDING_API_KEY')
        qdrant_url = os.getenv('QDRANT_API')
        qdrant_key = os.getenv('QDRANT_API_KEY')

        if not emb_model:
            raise ValueError("Brak zmiennej EMBEDDING_MODEL w pliku .env")

        # 1. Inicjalizacja klienta bazy wektorowej Qdrant
        _qdrant_client = qdrant_client.QdrantClient(
            url=qdrant_url,
            api_key=qdrant_key,
        )

        # 2. Inicjalizacja modelu Embeddingów (OpenAI lub Local/Nomic)
        # check_embedding_ctx_length=False pozwala na dłuższe teksty (ważne przy RAG)
        _embeddings = OpenAIEmbeddings(
            model=emb_model,
            base_url=emb_url,
            api_key=emb_key,
            check_embedding_ctx_length=False
        )
        print(f"[ISO Tool] Połączono z Qdrant i skonfigurowano Embeddingi ({emb_model}).", file=sys.stderr)

    except Exception as e:
        print(f"[ISO Tool] Błąd krytyczny inicjalizacji: {e}", file=sys.stderr)
        raise e


def run_iso_rag(query: str) -> str:
    """
    ### GŁÓWNA LOGIKA NARZĘDZIA RAG

    1. Zamienia pytanie tekstowe na wektor (Embedding).
    2. Szuka w bazie Qdrant wektorów najbardziej podobnych (Search).
    3. Zwraca surowy tekst dokumentacji wraz z metadanymi.
    """
    collection_name = os.getenv("COLLECTION_NAME")
    top_k = 100  # Ilość zwracanych fragmentów

    # Upewnij się, że mamy połączenie z bazą
    _init_resources()

    if not _qdrant_client or not _embeddings:
        return "Błąd techniczny: Narzędzie RAG nie jest poprawnie skonfigurowane."

    print(f"[RAG] Szukam: '{query}' w kolekcji '{collection_name}'", file=sys.stderr)

    try:
        # LangChain wrapper na Qdranta - ułatwia wyszukiwanie
        vector_store = QdrantVectorStore(
            client=_qdrant_client,
            collection_name=collection_name,
            embedding=_embeddings
        )

        # Tworzymy obiekt Retrievera i wykonujemy zapytanie
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.invoke(query)

        if not docs:
            return "Nie znaleziono relewantnych dokumentów w bazie wiedzy ISO 20022."

        # Formatowanie wyniku dla LLM-a
        # Ważne: Dodajemy informacje o źródle (Source File), aby LLM mógł zacytować plik.
        formatted_results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source_file", "nieznany plik")
            content = doc.page_content.strip()
            formatted_results.append(f"--- FRAGMENT {i} (Źródło: {source}) ---\n{content}")

        return "\n\n".join(formatted_results)

    except Exception as e:
        err_msg = f"Błąd podczas przeszukiwania bazy wiedzy: {str(e)}"
        print(f"[RAG Error] {err_msg}", file=sys.stderr)
        return err_msg