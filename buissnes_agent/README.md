
# ISO 20022 RAG Analyst Agent (MCP Architecture)

Zaawansowany system analityczny wykorzystujący architekturę **MCP (Model Context Protocol)** oraz technikę **RAG (Retrieval-Augmented Generation)**. System służy do analizy dokumentacji technicznej i biznesowej (głównie standard ISO 20022 / CBPR+), działając w oparciu o lokalne modele językowe (np. Hermes 70B) oraz bazę wektorową Qdrant.

Projekt rozdziela logikę na **Serwer MCP** (udostępniający narzędzia i wiedzę) oraz **Klienta** (Agenta LangGraph decydującego o ich użyciu).

---

## Kluczowe Funkcjonalności

*   **Architektura Client-Server (MCP):** Separacja bazy wiedzy od logiki agenta. Serwer udostępnia narzędzia, klient (Agent) z nich korzysta.
*   **Modułowy ETL & Chunking:** Możliwość dynamicznej zmiany strategii podziału tekstu za pomocą `.env`:
    *   *Legacy:* Prosty podział na zdania/paragrafy.
    *   *LangChain Advanced:* `MarkdownHeaderTextSplitter`, `SemanticChunker`, `RecursiveCharacterTextSplitter`.
*   **Local-First AI:** Domyślna konfiguracja pod **LM Studio** (model Hermes-4-70B) oraz lokalne embeddingi (**Nomic Embed**). Pełna kompatybilność z OpenAI.
*   **Baza Wektorowa Qdrant:** Przechowywanie i wyszukiwanie semantyczne fragmentów dokumentacji.
*   **LangGraph Agent:** Klient wyposażony w pamięć (`MemorySaver`) i pętlę decyzyjną ReAct.

---

## Wymagane biblioteki

```bash
pip install mcp[cli] uvicorn
pip install langchain langchain-core langchain-openai langchain-qdrant langchain-text-splitters langchain-experimental langchain-community
pip install langgraph qdrant-client python-dotenv
pip install httpx pypdf pandas openpyxl python-docx tiktoken scipy
```

---

## Konfiguracja i Uruchomienie

### 1. Baza danych i LLM

1.  **Uruchom Qdrant (Docker Compose):**
    Upewnij się, że masz plik `docker-compose.yaml`.
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
# Nazwa kolekcji (zmiana nazwy wymusi przeładowanie plików)
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
# "langchain" (nowy moduł) lub "legacy" (stary moduł)
CHUNKING_MODULE=langchain
# Strategie: markdown_header, semantic, recursive
CHUNKING_STRATEGY=markdown_header
CHUNK_SIZE=600
```

### 3. Dane wejściowe
Umieść swoje pliki (`.pdf`, `.md`, `.txt`, `.docx`) w folderze:
`./inputs`

---

## Jak uruchomić?

System składa się z dwóch elementów. Klient automatycznie uruchomi serwer w tle, ale warto wiedzieć jak działają.

### Krok 1: Weryfikacja Serwera (Opcjonalne)
Możesz uruchomić serwer ręcznie, aby sprawdzić, czy poprawnie indeksuje pliki (ETL):

```bash
python iso_server.py
```
*Jeśli zobaczysz "Starting ISO20022 RAG MCP Server...", to znaczy, że baza jest gotowa. Możesz zamknąć ten proces (Ctrl+C).*

### Krok 2: Uruchomienie Klienta (Czat)
To jest główny punkt wejścia do rozmowy.

```bash
python client.py
```

---

## Schemat działania (Architecture Flow)

1.  **Użytkownik** zadaje pytanie w `client.py`.
2.  **Agent (LangGraph)** analizuje pytanie przy użyciu modelu **Hermes-70B**.
3.  Jeśli pytanie wymaga wiedzy (np. "Co to jest pacs.008?"), Agent decyduje się użyć narzędzia `query_iso20022_knowledge_base`.
4.  **Klient MCP** wysyła żądanie JSON-RPC do **Serwera MCP** (`iso_server.py`).
5.  **Serwer MCP**:
    *   Zamienia pytanie na wektor (korzystając z **Nomic Embeddings**).
    *   Przeszukuje bazę **Qdrant**.
    *   Zwraca najlepiej dopasowane fragmenty tekstu.
6.  **Agent** otrzymuje kontekst i generuje finalną odpowiedź dla użytkownika.

---

## Struktura Plików

*   `client.py` - Klient terminalowy (Agent LangGraph), który rozmawia z użytkownikiem.
*   `iso_server.py` - Serwer MCP. Udostępnia narzędzia RAG, ale nie zawiera logiki decyzyjnej.
*   `SearchKnowledgebase.py` - Logika ETL. Skanuje folder, tnie pliki i wysyła do Qdranta.
*   `chunk_2.py` - Nowoczesny moduł podziału tekstu (Adapter LangChain).
*   `chunking.py` - Klasyczny moduł podziału tekstu (Wsteczna kompatybilność).
*   `config.py` - Ładowanie konfiguracji i inicjalizacja singletonów.