import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from vector_store import QdrantStore

# Konfiguracja podstawowego logowania
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

load_dotenv()

KNOWLEDGE_BASE = None


def get_knowledge_base():
    """
    Singleton Pattern: Tworzy lub zwraca istniejącą instancję SearchKnowledgebase.
    Odpowiada za wstrzyknięcie zależności (Client, Store, Config).
    """
    global KNOWLEDGE_BASE
    if KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE

    # Lazy import - zapobiega błędom cyklicznego importu
    from SearchKnowledgebase import SearchKnowledgebase

    # 1. Konfiguracja Chunkera
    chunk_module = os.getenv("CHUNKING_MODULE")  # domyślnie legacy
    chunk_strategy = os.getenv("CHUNKING_STRATEGY")  # domyślnie auto
    data_source = os.getenv("DATA_SOURCE")  # domyślnie auto

    try:
        chunk_size = int(os.getenv("CHUNK_SIZE", "600"))
    except ValueError:
        chunk_size = 600

    # 2. Konfiguracja Wymiaru Embeddings
    # OpenAI text-embedding-3-small/large = 1536, Nomic/Titan = 768
    try:
        emb_dim = int(os.getenv("EMBEDDING_DIM", "1536"))
    except ValueError:
        emb_dim = 1536

    # 3. Inicjalizacja Klientów
    client = OpenAI(
        api_key=os.getenv("EMBEDDING_API_KEY"),
        base_url=os.getenv("EMBEDDING_BASE_URL")
    )

    store = QdrantStore(
        url=os.getenv("QDRANT_API"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("COLLECTION_NAME", "knowledgebase"),
        vector_size=emb_dim
    )

    logger.info(f"Initializing KnowledgeBase. Module: {chunk_module}, Strategy: {chunk_strategy}")

    # 4. Instancjalizacja Głównego Orkiestratora
    KNOWLEDGE_BASE = SearchKnowledgebase(
        client=client,
        input_directory=os.getenv("INPUT_DIRECTORY", "./data"),
        input_s3_directory=os.getenv("INPUT_S3_DIRECTORY", ""),  # Pusty string jeśli nie używamy S3
        vector_store=store,
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        chunk_module=chunk_module,
        chunk_strategy=chunk_strategy,
        data_source_type=data_source,
        chunk_size=chunk_size,
        force_refresh=False  # Ustaw True w .env lub tutaj, aby wymusić przeładowanie bazy
    )
    return KNOWLEDGE_BASE


# Automatyczna inicjalizacja przy starcie aplikacji (import time)
try:
    get_knowledge_base()
except Exception as e:
    # Logujemy błąd krytyczny, ale pozwalamy aplikacji działać (np. w trybie offline)
    logger.error(f"CRITICAL INIT ERROR: Nie udało się zainicjować bazy wiedzy: {e}")