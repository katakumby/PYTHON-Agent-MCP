import sys
import asyncio
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# IMPORTY LOGIKI NARZĘDZI
from tools.tool_iso_rag import run_iso_rag
from tools.tool_wikipedia import run_wikipedia_search
from tools.tool_confluence import run_confluence_search

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Wyciszenie logów bibliotek HTTP (zbyt gadatliwe)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

load_dotenv()

# Inicjalizacja instancji FastMCP (nazwa serwera widoczna dla klienta)
mcp = FastMCP("ISO20022 RAG Analyst Service")


# ==============================================================================
# DEFINICJA NARZĘDZI MCP (Tool Registration)
# ==============================================================================

@mcp.tool()
async def query_iso20022_knowledge_base(query: str) -> str:
    """
    Wyszukuje informacje w bazie wiedzy ISO 20022 (specyfikacje techniczne, XML, pola, CBPR+).
    Użyj tego narzędzia do pytań o:
    - Strukturę komunikatów (pacs, camt, pain).
    - Tagi XML i reguły walidacji.
    - Standardy SWIFT CBPR+.
    """
    # WAŻNE: asyncio.to_thread uruchamia funkcję synchroniczną (run_iso_rag) w osobnym wątku.
    # Zapobiega to blokowaniu pętli zdarzeń (Event Loop) serwera, gdy czekamy na bazę danych.
    return await asyncio.to_thread(run_iso_rag, query)


@mcp.tool()
async def search_wikipedia_general(query: str) -> str:
    """
    Przeszukuje Wikipedię w celu znalezienia definicji ogólnych, historii, kodów krajów itp.
    Użyj tego narzędzia do pytań nietechnicznych:
    - Definicje biznesowe (np. "Co to jest IBAN?").
    - Informacje o organizacjach (SWIFT, FED, EBA).
    - Dane geograficzne i historyczne.
    """
    return await asyncio.to_thread(run_wikipedia_search, query)


@mcp.tool()
async def search_confluence_internal(query: str) -> str:
    """
    Przeszukuje wewnętrzną dokumentację firmy w Confluence.
    Użyj tego narzędzia do pytań o:
    - Procedury operacyjne ("Jak my to robimy?").
    - Ustalenia projektowe i notatki ze spotkań.
    - Specyfikę wdrożenia systemów w organizacji.
    """
    return await asyncio.to_thread(run_confluence_search, query)


# ==============================================================================
# URUCHOMIENIE SERWERA (Entry Point)
# ==============================================================================

if __name__ == "__main__":
    import argparse

    # 1. Obsługa procesu ETL (Ingestia Danych)
    # Próba załadowania pliku config.py, który (w starej architekturze) uruchamiał indeksowanie plików.
    # Jest to opcjonalne, aby serwer działał nawet jeśli ETL się nie powiedzie.
    try:
        import config

        print("[Server] Konfiguracja ETL załadowana pomyślnie.", file=sys.stderr)
    except ImportError:
        pass  # Ignorujemy brak configu
    except Exception as e:
        print(f"[Server] Ostrzeżenie: Błąd podczas ładowania ETL: {e}", file=sys.stderr)

    # 2. Konfiguracja argumentów linii poleceń (CLI Args)
    # Pozwala to na elastyczne uruchamianie serwera w różnych trybach architektury A2A.
    parser = argparse.ArgumentParser(description="Uruchamia serwer MCP dla Agenta ISO 20022")

    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"],
                        help="Tryb transportu: 'stdio' (lokalny pipe, domyślny) lub 'sse' (HTTP server)")
    parser.add_argument("--port", default=8000, type=int,
                        help="Port nasłuchiwania dla trybu SSE (domyślnie 8000)")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host nasłuchiwania dla trybu SSE (domyślnie wszystkie interfejsy)")

    # parse_known_args jest bezpieczniejsze niż parse_args, bo FastMCP może używać własnych flag
    args, _ = parser.parse_known_args()

    print(f"Starting ISO20022 RAG MCP Server in mode: {args.transport.upper()}...", file=sys.stderr)

    # 3. Wybór trybu uruchomienia
    if args.transport == "sse":
        # Tryb SSE: Serwer HTTP (np. dla komunikacji między kontenerami Docker)
        # Uruchomienie: python iso_server.py --transport sse
        mcp.host = args.host
        mcp.port = args.port
        mcp.run(transport="sse")
    else:
        # Tryb STDIO: Komunikacja przez standardowe wejście/wyjście.
        # Domyślny tryb dla klientów lokalnych (np. Claude Desktop App lub nasz client.py)
        mcp.run(transport="stdio")


        # Prompty testowe
        # RAG
        # Wymień pola obowiązkowe w bloku Group Header dla komunikatu pacs.008 zgodnie ze specyfikacją CBPR+.
        # Jaki jest maksymalny limit znaków dla pola EndToEndIdentification i czy dozwolone są w nim znaki specjalne?
        # Wyjaśnij, czego dotyczy reguła walidacyjna VR00060 w kontekście komunikatu pacs.008.
        # Czy blok 'Remittance Information' jest obowiązkowy w komunikacie camt.053 i jakie pod-pola zawiera w wersji 001.08?
        # Wikipedia
        # Kiedy powstała organizacja SWIFT i gdzie znajduje się jej główna siedziba?
        # Confluence
        # Jak wygląda nasza wewnętrzna procedura walidacji komunikatów płatniczych przed wysyłką?
        # hybryda
        # Co to jest komunikat camt.053 i jak go archiwizujemy w naszym systemie?