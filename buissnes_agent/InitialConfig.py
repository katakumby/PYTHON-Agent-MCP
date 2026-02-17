import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from QdrantDatabaseStore import QdrantDatabaseStore

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
    from KnowledgebasePipeline import SearchKnowledgebase

    # 1. Konfiguracja Chunkera
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

    # =========================================================
    # DYNAMICZNY IMPORT LOADERA (Warstwa Danych)
    # =========================================================
    # Importujemy klasę dopiero tutaj, wewnątrz IF-a.
    # Dzięki temu nie musimy mieć boto3, jeśli używamy 'local'.

    data_loader = None

    if data_source == "s3":
        logger.info("Dynamic Import: Ładowanie modułu S3...")
        # Import wewnątrz funkcji!
        from DataLoaderS3FileLoader import DataLoaderS3FileLoader

        data_loader = DataLoaderS3FileLoader(
            bucket_name=os.getenv("S3_BUCKET"),
            prefix=os.getenv("INPUT_S3_DIRECTORY", "")
        )
    else:
        logger.info("Dynamic Import: Ładowanie modułu LocalFile...")
        # Import wewnątrz funkcji!
        from DataLoaderLocalFileLoader import DataLoaderLocalFileLoader

        data_loader = DataLoaderLocalFileLoader(
            directory=os.getenv("INPUT_DIRECTORY", "./data")
        )

    # 3. Inicjalizacja Klientów
    client = OpenAI(
        api_key=os.getenv("EMBEDDING_API_KEY"),
        base_url=os.getenv("EMBEDDING_BASE_URL")
    )

    store = QdrantDatabaseStore(
        url=os.getenv("QDRANT_API"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("COLLECTION_NAME", "knowledgebase"),
        vector_size=emb_dim
    )

    # 4. Instancjalizacja Głównego Orkiestratora
    KNOWLEDGE_BASE = SearchKnowledgebase(
        client=client,
        database_store=store,
        data_loader=data_loader,
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        force_refresh=False  # Ustaw True w .env lub tutaj, aby wymusić przeładowanie bazy
    )
    return KNOWLEDGE_BASE


# Automatyczna inicjalizacja przy starcie aplikacji (import time)
try:
    get_knowledge_base()
except Exception as e:
    # Logujemy błąd krytyczny, ale pozwalamy aplikacji działać (np. w trybie offline)
    logger.error(f"CRITICAL INIT ERROR: Nie udało się zainicjować bazy wiedzy: {e}")