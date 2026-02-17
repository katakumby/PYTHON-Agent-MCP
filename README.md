# ISO 20022 RAG Analyst Agent (MCP Architecture)

Zaawansowany system analityczny wykorzystujący architekturę **MCP (Model Context Protocol)** oraz technikę **RAG (Retrieval-Augmented Generation)**. System służy do analizy dokumentacji technicznej i biznesowej (głównie standard ISO 20022 / CBPR+), działając w oparciu o lokalne modele językowe (np. Hermes 70B) oraz bazę wektorową Qdrant.

Projekt rozdziela logikę na **Serwer MCP** (udostępniający narzędzia i wiedzę) oraz **Klienta** (Agenta LangGraph decydującego o ich użyciu).

---

## Kluczowe Funkcjonalności

*   **Architektura Client-Server (MCP):** Separacja bazy wiedzy od logiki agenta. Obsługa transportu **STDIO** (lokalnie) oraz **SSE** (HTTP/Sieć).
*   **Modułowy ETL & Chunking:** Możliwość dynamicznej zmiany strategii podziału tekstu za pomocą `.env`:
    *   *Legacy:* Prosty podział na zdania/paragrafy.
    *   *LangChain Advanced:* `MarkdownHeaderTextSplitter`, `SemanticChunker`, `RecursiveCharacterTextSplitter`.
*   **Local-First AI:** Domyślna konfiguracja pod **LM Studio** (model Hermes-4-70B) oraz lokalne embeddingi (**Nomic Embed**). Pełna kompatybilność z OpenAI.
*   **Baza Wektorowa Qdrant:** Przechowywanie i wyszukiwanie semantyczne fragmentów dokumentacji.
*   **LangGraph Agent:** Klient wyposażony w pamięć (`MemorySaver`) i pętlę decyzyjną ReAct.

---

## Wymagane biblioteki

Bez uv
```bash
pip install mcp[cli] uvicorn sse-starlette
pip install langchain langchain-core langchain-openai langchain-qdrant langchain-text-splitters langchain-experimental langchain-community
pip install langgraph qdrant-testscripts python-dotenv
pip install httpx pypdf pandas openpyxl python-docx tiktoken scipy
pip install wikipedia atlassian-python-api fastmcp
```

Z użyciem uv
```bash
uv sync
```

---

## Konfiguracja

### 1. Baza danych i LLM

1.  **Uruchom Qdrant (Docker Compose):**
    ```bash
    docker compose up -d
    ```
2.  **Uruchom LM Studio (Serwer Lokalny):**
    *   Załaduj model LLM (np. `Hermes-4-70B`).
    *   Załaduj model Embeddingów (np. `nomic-embed-text-v1.5`).
    *   Uruchom serwer na porcie `1234`.

### 2. Konfiguracja `.env`

Stwórz plik `.env` w katalogu głównym:

```ini
# --- QDRANT ---
QDRANT_API=http://localhost:6333
QDRANT_API_KEY=
COLLECTION_NAME=iso20022_v1
INPUT_DIRECTORY=./inputs

# --- EMBEDDINGS (LM Studio / Nomic) ---
EMBEDDING_BASE_URL=http://localhost:1234/v1
EMBEDDING_API_KEY=lm-studio
EMBEDDING_MODEL=nomic-embed-text-v1.5
EMBEDDING_DIM=768

# --- CHAT LLM (LM Studio / Hermes) ---
CHAT_BASE_URL=http://localhost:1234/v1
CHAT_API_KEY=lm-studio
CHAT_MODEL=Hermes-4-70B

# --- KONFIGURACJA CHUNKINGU ---
CHUNKING_MODULE=langchain
CHUNKING_STRATEGY=markdown_header
CHUNK_SIZE=600
```

---

## Tryby Uruchamiania (How to Run)

System wspiera dwa modele architektury zgodne ze standardem MCP.
### Opcja 1: Tryb Lokalny (STDIO) – Domyślny
W tym trybie Klient automatycznie uruchamia Serwer jako podproces w tle. Komunikacja odbywa się przez standardowe wejście/wyjście. Jest to najprostsza metoda do szybkiego testowania ("Zero Config").

1.  Upewnij się, że w pliku `client_for_MCP_test.py` zmienna transportu ustawiona jest na:
    ```python
    selected_transport = "stdio"
    ```
2.  Uruchom klienta:
    ```bash
    python testscripts.py
    ```
    *Klient sam zadba o uruchomienie i zamknięcie serwera.*

### Opcja 2: Tryb Sieciowy (A2A / SSE) – Zaawansowany
Symulacja architektury rozproszonej (Agent-to-Agent). Serwer działa jako niezależna usługa HTTP, a Klient łączy się do niego przez sieć. Pozwala to na hostowanie Agenta i Bazy Wiedzy na różnych maszynach/kontenerach.

**Krok 1: Uruchom Serwer (Terminal 1)**
Uruchom serwer wskazując transport `sse` oraz port:
```bash
python buissnes_agent/MCPServer.py --transport sse --port 8000
# lub
uv run buissnes_agent/MCPServer.py --transport sse --port 8000

```
*Serwer rozpocznie nasłuchiwanie na `http://0.0.0.0:8000/sse`.*

**Krok 2: Skonfiguruj i Uruchom Klienta (Terminal 2)**
1.  Edytuj plik `client_for_MCP_test.py` i zmień tryb transportu:
    ```python
    selected_transport = "sse"
    # Upewnij się, że port w funkcji init_session to 10000
    ```
2.  Uruchom klienta:
    ```bash
    python test_script_client_for_MCP.py
    ```
    *Klient nawiąże połączenie HTTP z działającym serwerem.*

---

## Schemat działania (Architecture Flow)

1.  **Użytkownik** zadaje pytanie w `client_for_MCP_test.py`.
2.  **Agent (LangGraph)** analizuje pytanie przy użyciu modelu **Hermes-70B**.
3.  Jeśli pytanie wymaga wiedzy (np. "Co to jest pacs.008?"), Agent decyduje się użyć narzędzia `query_iso20022_knowledge_base`.
4.  **Klient MCP** wysyła żądanie JSON-RPC do **Serwera MCP** (`iso_server.py`) – albo przez potok STDIO, albo przez HTTP (SSE).
5.  **Serwer MCP**:
    *   Zamienia pytanie na wektor (korzystając z **Nomic Embeddings**).
    *   Przeszukuje bazę **Qdrant**.
    *   Zwraca najlepiej dopasowane fragmenty tekstu wraz z metadanymi (źródło pliku).
6.  **Agent** otrzymuje kontekst i generuje finalną odpowiedź dla użytkownika.

---

## Struktura Plików

*   `client_for_MCP_test.py` - Klient Agenta LangGraph. Obsługuje logikę decyzyjną i łączy się z serwerem MCP (STDIO/SSE).
*   `iso_server.py` - Serwer MCP. Udostępnia endpointy i narzędzia RAG. Obsługuje flagi CLI (`--transport`, `--port`).
*   `SearchKnowledgebase.py` - Logika ETL. Skanuje folder, tnie pliki i wysyła do Qdranta.
*   `chunking_lang_graph.py` - Nowoczesny moduł podziału tekstu (Adapter LangChain).
*   `config.py` - Ładowanie konfiguracji i inicjalizacja singletonów.