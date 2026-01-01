import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from vector_store import QdrantStore

load_dotenv()
logger = logging.getLogger(__name__)

KNOWLEDGE_BASE = None


def get_knowledge_base():
    global KNOWLEDGE_BASE
    if KNOWLEDGE_BASE: return KNOWLEDGE_BASE

    from SearchKnowledgebase import SearchKnowledgebase

    # Pobranie konfiguracji chunkera
    chunk_module = os.getenv("CHUNKING_MODULE")
    chunk_strategy = os.getenv("CHUNKING_STRATEGY")

    # Obsługa wymiaru wektora (Nomic=768)
    try:
        emb_dim = int(os.getenv("EMBEDDING_DIM"))
    except:
        emb_dim = 768

    client = OpenAI(
        api_key=os.getenv("EMBEDDING_API_KEY"),
        base_url=os.getenv("EMBEDDING_BASE_URL")
    )

    store = QdrantStore(
        url=os.getenv("QDRANT_API"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("COLLECTION_NAME"),
        vector_size=emb_dim
    )

    KNOWLEDGE_BASE = SearchKnowledgebase(
        client=client,
        input_directory=os.getenv("INPUT_DIRECTORY"),
        vector_store=store,
        embedding_model=os.getenv("EMBEDDING_MODEL"),
        chunk_module=chunk_module,
        chunk_strategy=chunk_strategy,
        force_refresh=False  # Ustaw True by przeładować pliki
    )
    return KNOWLEDGE_BASE


# Uruchomienie przy imporcie (zbuduje bazę jeśli pusta)
try:
    KNOWLEDGE_BASE = get_knowledge_base()
except Exception as e:
    logger.error(f"Init Error: {e}")