import logging
import sys

from openai import OpenAI

from QdrantDatabaseStore import QdrantDatabaseStore
from buissnes_agent.config_loader import settings

# Konfiguracja podstawowego logowania
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

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
    data_source = settings.get("data_source.type", "local")

    # 2. Konfiguracja Wymiaru Embeddings
    # OpenAI text-embedding-3-small/large = 1536, Nomic/Titan = 768
    emb_dim = settings.get("vector_db.dimension", 1536)

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
            bucket_name=settings.get("data_source.s3.bucket"),
            prefix=settings.get("data_source.s3.prefix")
        )
    else:
        logger.info("Dynamic Import: Ładowanie modułu LocalFile...")
        # Import wewnątrz funkcji!
        from DataLoaderLocalFileLoader import DataLoaderLocalFileLoader

        data_loader = DataLoaderLocalFileLoader(
            directory=settings.get("data_source.local_input_path")
        )

    # 3. Inicjalizacja Klientów
    client = OpenAI(
        # api_key=os.getenv("EMBEDDING_API_KEY"),
        api_key=settings.get("llm.embedding.api_key"),
        base_url=settings.get("llm.embedding.base_url")
    )

    store = QdrantDatabaseStore(
        url=settings.get("vector_db.url"),
        api_key=settings.get("vector_db.api_key"),
        collection_name=settings.get("vector_db.collection_name"),
        vector_size=emb_dim
    )

    # 4. Instancjalizacja Głównego Orkiestratora
    KNOWLEDGE_BASE = SearchKnowledgebase(
        client=client,
        database_store=store,
        data_loader=data_loader,
        embedding_model=settings.get("llm.embedding.model"),
        force_refresh=False  # Ustaw True w .env lub tutaj, aby wymusić przeładowanie bazy
    )
    return KNOWLEDGE_BASE


# Automatyczna inicjalizacja przy starcie aplikacji (import time)
try:
    get_knowledge_base()
except Exception as e:
    # Logujemy błąd krytyczny, ale pozwalamy aplikacji działać (np. w trybie offline)
    logger.error(f"CRITICAL INIT ERROR: Nie udało się zainicjować bazy wiedzy: {e}")