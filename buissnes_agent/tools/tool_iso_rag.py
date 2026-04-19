import logging
import os
import sys
import time
from typing import Optional, Tuple

import qdrant_client
from dotenv import load_dotenv
from buissnes_agent.EmbeddingClient import LocalEmbeddingClient

# ===== METRYKI: IMPORT =====
try:
    from buissnes_agent.tools.rag_metrics import (
        MetricsCalculator,
        RetrievalMetrics,
        metrics_collector,
    )
except ImportError:
    from tools.rag_metrics import (  # type: ignore
        MetricsCalculator,
        RetrievalMetrics,
        metrics_collector,
    )
# ===========================

logger = logging.getLogger(__name__)
DEFAULT_VECTOR_AMOUNT_RAG = 10

# ==============================================================================
# ZASOBY GLOBALNE (SINGLETONY)
# ==============================================================================
# Przechowujemy instancje klienta Qdrant i modelu Embeddingów globalnie,
# aby nie tworzyć nowego połączenia przy każdym zapytaniu (optymalizacja).
_qdrant_client: Optional[qdrant_client.QdrantClient] = None
_embeddings: Optional[LocalEmbeddingClient] = None

load_dotenv()

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
        # Pobranie konfiguracji Qdrant z .env
        qdrant_url = os.getenv('QDRANT_API')
        qdrant_key = os.getenv('QDRANT_API_KEY')

        # Weryfikacja tylko dla Qdranta, bo LocalEmbeddingClient sam sprawdza swoje zmienne
        if not qdrant_url:
            raise ValueError("Brak zmiennej QDRANT_API w pliku .env")

        # 1. Inicjalizacja klienta bazy wektorowej Qdrant
        logger.info(f"Łączenie z Qdrant: {qdrant_url}")
        _qdrant_client = qdrant_client.QdrantClient(
            url=qdrant_url,
            api_key=qdrant_key,
            # timeout=60 # Opcjonalnie można zwiększyć timeout
        )

        # 2. Inicjalizacja modelu Embeddingów (Local Embedding Client)
        # Klasa sama zaciąga: EMBEDDING_BASE_URL, EMBEDDING_API_KEY, EMBEDDING_MODEL z .env
        # oraz automatycznie naprawia błędy 400 Bad Request.
        logger.info("Inicjalizacja LocalEmbeddingClient...")
        _embeddings = LocalEmbeddingClient()

        print(f"[ISO Tool] Połączono z Qdrant i skonfigurowano Embeddingi ({_embeddings.model}).", file=sys.stderr)

    except Exception as e:
        err_msg = f"[ISO Tool] Błąd krytyczny inicjalizacji zasobów: {e}"
        print(err_msg, file=sys.stderr)
        logger.error(err_msg)
        raise e

# ==============================================================================
# METODY POMOCNICZE METRYK (wydzielone)
# ==============================================================================

def _measure_embedding_time(embedder, query: str) -> Tuple[list, int]:
    """
    Generuje embedding z pomiarem czasu

    Returns:
        tuple: (query_vector, embedding_latency_ms)
    """
    start_time = time.time()
    query_vector = embedder.embed_query(query)
    latency_ms = MetricsCalculator.calculate_latency_ms(start_time)
    return query_vector, latency_ms


def _measure_search_time(client, collection_name: str, query_vector: list, top_k: int):
    """
    Wykonuje search z pomiarem czasu

    Returns:
        tuple: (search_response, search_latency_ms)
    """
    start_time = time.time()
    search_response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    latency_ms = MetricsCalculator.calculate_latency_ms(start_time)
    return search_response, latency_ms


def resolve_top_k(top_k: int | None = None) -> int:
    """
    Resolve the effective retrieval limit.

    Explicit top_k takes precedence. When it is not provided, the function
    falls back to VECTOR_AMOUNT_RAG from the environment and then to the code
    default.
    """
    if top_k is not None:
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer when provided.")
        return top_k

    env_value = (os.getenv("VECTOR_AMOUNT_RAG") or "").strip()
    if not env_value:
        return DEFAULT_VECTOR_AMOUNT_RAG

    try:
        resolved_top_k = int(env_value)
    except ValueError:
        logger.warning(
            "Invalid VECTOR_AMOUNT_RAG=%r. Falling back to %s.",
            env_value,
            DEFAULT_VECTOR_AMOUNT_RAG,
        )
        return DEFAULT_VECTOR_AMOUNT_RAG

    if resolved_top_k <= 0:
        logger.warning(
            "Non-positive VECTOR_AMOUNT_RAG=%r. Falling back to %s.",
            env_value,
            DEFAULT_VECTOR_AMOUNT_RAG,
        )
        return DEFAULT_VECTOR_AMOUNT_RAG

    return resolved_top_k


def _format_search_results(points) -> str:
    """
    Formatuje wyniki wyszukiwania do czytelnego tekstu

    Args:
        points: Lista punktów z Qdrant

    Returns:
        str: Sformatowany output
    """
    formatted_output = []

    for i, point in enumerate(points, 1):
        payload = point.payload or {}

        # Ekstrakcja pól z payloadu
        content = payload.get("phrase") or payload.get("text") or "[BRAK TREŚCI]"
        title = payload.get("title", "Bez tytułu")
        source_path = payload.get("source", "Nieznane źródło")
        url = payload.get("url", "-")
        domain = payload.get("domain", "ogólna")
        extension = payload.get("extension", "")
        meta_id = payload.get("phrase_metadata_id", "brak-id")

        tags_list = payload.get("tags", [])
        tags_str = ", ".join(tags_list) if isinstance(tags_list, list) else str(tags_list)

        page = payload.get("page_number")
        page_info = f", Strona: {page}" if page else ""
        start_byte = payload.get("start_byte")
        end_byte = payload.get("end_byte")
        byte_range = None
        if isinstance(start_byte, int):
            byte_range = (
                f"bytes={start_byte}-"
                if not isinstance(end_byte, int)
                else f"bytes={start_byte}-{end_byte}"
            )

        entry_lines = [
            f"--- DOKUMENT {i} (Relewancja: {point.score:.4f}) ---",
            f"Tytuł: {title}",
            f"Źródło (plik): {source_path}{page_info}",
        ]
        if byte_range:
            entry_lines.append(f"Zakres bajtów: {byte_range}")
        entry_lines.extend(
            [
                f"URL: {url}",
                f"Domena: {domain}",
                f"Typ: {extension}",
                f"Tagi: {tags_str}",
                f"ID Fragmentu: {meta_id}",
                f"Treść:\n{content.strip()}",
            ]
        )
        entry = "\n".join(entry_lines)
        formatted_output.append(entry)

    return "\n\n".join(formatted_output)


# ==============================================================================
# GŁÓWNA FUNKCJA RAG Z METRYKAMI
# ==============================================================================

def run_generic_rag_with_metrics(
        query: str,
        collection_name: str,
        top_k: int | None = None,
) -> Tuple[str, Optional[RetrievalMetrics]]:
    """
    RAG z pełnymi metrykami retrieval (jeśli włączone w ENV)

    Args:
        query: Pytanie użytkownika
        collection_name: Nazwa kolekcji w Qdrant

    Returns:
        tuple: (formatted_output, retrieval_metrics)
               Jeśli ENABLE_RAG_METRICS=false, metrics będzie None
    """
    # Start timer dla całego procesu
    total_start = time.time()

    top_k = resolve_top_k(top_k)

    # ===== OBSŁUGA BŁĘDÓW INICJALIZACJI =====
    try:
        _init_resources()
    except Exception as e:
        error_msg = f"Błąd techniczny: Nie udało się połączyć z bazą wiedzy ({str(e)})."
        total_latency = MetricsCalculator.calculate_latency_ms(total_start)

        # Twórz metryki tylko jeśli włączone
        error_metrics = None
        if metrics_collector.is_enabled():
            error_metrics = MetricsCalculator.create_error_metrics(
                query=query,
                collection_name=collection_name,
                latency_ms=total_latency
            )
            metrics_collector.log_retrieval(error_metrics)

        return error_msg, error_metrics

    client = _qdrant_client
    embedder = _embeddings

    if not client or not embedder:
        error_msg = "Błąd techniczny: Narzędzie RAG nie jest poprawnie skonfigurowane."
        total_latency = MetricsCalculator.calculate_latency_ms(total_start)

        error_metrics = None
        if metrics_collector.is_enabled():
            error_metrics = MetricsCalculator.create_error_metrics(
                query=query,
                collection_name=collection_name,
                latency_ms=total_latency
            )
            metrics_collector.log_retrieval(error_metrics)

        return error_msg, error_metrics

    print(f"[RAG] Szukam: '{query}' w kolekcji '{collection_name}'", file=sys.stderr)

    # ===== GŁÓWNA LOGIKA RETRIEVAL =====
    try:
        # KROK 1: Generowanie wektora zapytania (z pomiarem czasu)
        query_vector, embedding_latency = _measure_embedding_time(embedder, query)

        # KROK 2: Wyszukiwanie w Qdrant (z pomiarem czasu)
        search_response, search_latency = _measure_search_time(
            client, collection_name, query_vector, top_k
        )

        points = search_response.points

        # KROK 3: Obsługa pustych wyników
        if not points:
            no_results_msg = "Nie znaleziono relewantnych dokumentów w bazie wiedzy ISO 20022."
            total_latency = MetricsCalculator.calculate_latency_ms(total_start)

            empty_metrics = None
            if metrics_collector.is_enabled():
                empty_metrics = MetricsCalculator.create_retrieval_metrics(
                    query=query,
                    collection_name=collection_name,
                    points=None,
                    total_latency_ms=total_latency,
                    embedding_latency_ms=embedding_latency,
                    search_latency_ms=search_latency
                )
                metrics_collector.log_retrieval(empty_metrics)

            return no_results_msg, empty_metrics

        # KROK 4: Formatowanie wyników
        formatted_output = _format_search_results(points)

        # KROK 5: Tworzenie metryk (tylko jeśli włączone)
        total_latency = MetricsCalculator.calculate_latency_ms(total_start)

        metrics = None
        if metrics_collector.is_enabled():
            metrics = MetricsCalculator.create_retrieval_metrics(
                query=query,
                collection_name=collection_name,
                points=points,
                total_latency_ms=total_latency,
                embedding_latency_ms=embedding_latency,
                search_latency_ms=search_latency
            )
            metrics_collector.log_retrieval(metrics)

        return formatted_output, metrics

    except Exception as e:
        err_msg = f"Błąd podczas przeszukiwania bazy wiedzy: {str(e)}"
        print(f"[RAG Error] {err_msg}", file=sys.stderr)

        total_latency = MetricsCalculator.calculate_latency_ms(total_start)

        error_metrics = None
        if metrics_collector.is_enabled():
            error_metrics = MetricsCalculator.create_error_metrics(
                query=query,
                collection_name=collection_name,
                latency_ms=total_latency
            )
            metrics_collector.log_retrieval(error_metrics)

        return err_msg, error_metrics


# ==============================================================================
# BACKWARD COMPATIBILITY: Stara funkcja bez metryk
# ==============================================================================

def run_generic_rag(
    query: str,
    collection_name: str,
    top_k: int | None = None,
) -> str:
    """
    Oryginalna funkcja bez metryk (dla backward compatibility)

    Używa wewnętrznie run_generic_rag_with_metrics, ale zwraca tylko wynik.
    Metryki są nadal zbierane w tle (jeśli ENABLE_RAG_METRICS=true).
    """
    result, _ = run_generic_rag_with_metrics(
        query,
        collection_name,
        top_k=top_k,
    )
    return result
