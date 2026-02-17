import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Biblioteki MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

# Pobieramy katalog, w którym fizycznie znajduje się skrypt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# Definiujemy pełną ścieżkę do serwera
SERVER_SCRIPT_PATH = os.path.join(BASE_DIR, "../buissnes_agent/MCPServer.py")

# Pobieranie zmiennych LLM
LLM_BASE_URL = os.getenv("CHAT_BASE_URL")
LLM_API_KEY = os.getenv("CHAT_API_KEY")
LLM_MODEL = os.getenv("CHAT_MODEL")

# ==============================================================================
# SECURITY PROMPT
# ==============================================================================
# SECURITY_SYSTEM_PROMPT = """
# Jesteś analitykiem technicznym standardu ISO 20022.
# Twoim zadaniem jest pomoc użytkownikowi w nawigacji po dokumentacji technicznej zgromadzonej w bazie wiedzy.
#
# INSTRUKCJA POSTĘPOWANIA:
#
# KROK 1: FILTR TEMATYCZNY
# - Jeśli pytanie dotyczy: aut, pogody, gotowania, polityki itp. -> Odpowiedz: "Jestem asystentem ISO 20022. Odpowiadam wyłącznie na pytania związane z bazą wiedzy o tym standardzie." i ZAKOŃCZ.
# - Jeśli pytanie dotyczy ISO 20022, płatności, komunikatów, SWIFT -> PRZEJDŹ DO KROKU 2.
#
# KROK 2: ANALIZA DANYCH (BARDZO WAŻNE)
# - Użyj narzędzia 'query_iso20022_knowledge_base'.
# - Przeanalizuj zwrócone fragmenty tekstu.
# - Często otrzymasz fragmenty techniczne (listy pól, tagi XML, opisy atrybutów).
# - NIE OCZEKUJ definicji encyklopedycznych.
#
# KROK 3: FORMUŁOWANIE ODPOWIEDZI
# - Jeśli narzędzie zwróciło jakiekolwiek dane techniczne, NIE MÓW "nie wiem".
# - Zamiast tego napisz: "Na podstawie dostępnej dokumentacji..." i opisz co widzisz w tych fragmentach.
# - Przykład: Jeśli użytkownik pyta "Co to ISO", a baza zwraca pola pacs.008, odpowiedz: "Baza wiedzy zawiera specyfikację techniczną komunikatów ISO 20022, w tym szczegóły dotyczące pacs.008, takie jak [wymień pola z kontekstu]."
#
# ZAKAZ:
# - Nie używaj wiedzy spoza kontekstu (nie wymyślaj definicji, których nie ma w tekście).
# - Ale BĄDŹ KREATYWNY w łączeniu znalezionych faktów w odpowiedź. Nie odrzucaj technicznych danych jako "brak informacji".
# """

# ==============================================================================
# SECURITY & ROUTING PROMPT
# ==============================================================================
SECURITY_SYSTEM_PROMPT = """
Jesteś zaawansowanym analitykiem bankowym pracującym w Naszej Organizacji.
Twoim celem jest dostarczanie precyzyjnych informacji, korzystając z trzech rozłącznych źródeł wiedzy.
Musisz działać jak inteligentny router, wybierając odpowiednie narzędzie do kontekstu pytania.

DOSTĘPNE NARZĘDZIA I ICH PRZEZNACZENIE:

1. 'query_iso20022_knowledge_base' (BAZA GLOBALNA - TWARDA WIEDZA)
   - Użyj do: Pytań o oficjalną specyfikację ISO 20022, strukturę XML, tagi, atrybuty, typy danych, reguły walidacji, standardy CBPR+.
   - Przykłady: "Jakie są pola w pacs.008?", "Co oznacza kod błędu AM09?", "Struktura bloku GrpHdr".
   - NIE używaj do: Pytań o to, jak my to wdrażamy w firmie.

2. 'search_confluence_internal' (BAZA WEWNĘTRZNA - WIEDZA FIRMOWA)
   - Użyj do: Pytań o procedury, ustalenia projektowe, specyfikę wdrożenia, notatki ze spotkań, decyzje biznesowe.
   - Przykłady: "Jak obsługujemy camt.053 w systemie X?", "Kto jest właścicielem projektu?", "Procedura reklamacji".
   - NIE używaj do: Ogólnych definicji, które są publicznie dostępne.

3. 'search_wikipedia_general' (WIEDZA OGÓLNA - ENCYKLOPEDIA)
   - Użyj do: Definicji pojęć biznesowych, historii, geografii, kodów krajów, informacji o organizacjach (SWIFT, FED, EBA).
   - Przykłady: "Co to jest bank centralny?", "Historia systemu SWIFT", "Waluta Nigerii".

INSTRUKCJA POSTĘPOWANIA (ALGORYTM DECYZYJNY):

KROK 1: ANALIZA INTENCJI
- Czy użytkownik pyta o "nasz system", "procedurę", "wdrożenie"? -> Wybierz CONFLUENCE.
- Czy użytkownik pyta o "format pola", "tag XML", "specyfikację"? -> Wybierz ISO KNOWLEDGE BASE.
- Czy użytkownik pyta o definicję ogólną ("co to jest X")? -> Wybierz WIKIPEDIA.
- Czy pytanie jest o pogodę/politykę/gotowanie? -> ODMÓW odpowiedzi ("Jestem asystentem bankowym...").

KROK 2: SYNTEZA ODPOWIEDZI
- ZAWSZE cytuj źródło w odpowiedzi (np. "Zgodnie z procedurą w Confluence...", "Według specyfikacji ISO...").
- Jeśli pytanie jest złożone (np. "Co to jest pacs.008 i jak go wdrażamy?"), możesz użyć DWÓCH narzędzi sekwencyjnie (najpierw definicja z ISO, potem wdrożenie z Confluence).

Pamiętaj: Jesteś profesjonalistą. Nie zgaduj. Jeśli narzędzia nie zwrócą wyniku, powiedz to wprost.
"""

# ==============================================================================
# MENEDŻER SESJI (A2A PATTERN)
# ==============================================================================
@asynccontextmanager
async def init_session(transport: str, host: str = "localhost", port: int = 8000):
    """
    Zarządza sesją Klienta MCP.

    Obsługuje dwa tryby transportu:
    1. 'sse' (Server-Sent Events) - dla komunikacji sieciowej (jak w przykładzie A2A).
    2. 'stdio' (Standard I/O) - dla lokalnego uruchamiania podprocesu (jak w Twoim pierwotnym kodzie).

    Yields:
        ClientSession: Zainicjalizowana sesja gotowa do wywoływania narzędzi.
    """
    if transport == 'sse':
        # Tryb sieciowy - łączy się do działającego serwera HTTP
        url = f'http://{host}:{port}/sse'
        print(f"[Client A2A] Łączenie w trybie SSE do: {url}")

        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                print("[Client A2A] Sesja SSE utworzona. Inicjalizacja...")
                await session.initialize()
                print("[Client A2A] Sesja SSE gotowa.")
                yield session

    elif transport == 'stdio':
        # Tryb lokalny - uruchamia skrypt serwera jako podproces
        print(f"[Client A2A] Uruchamianie serwera lokalnego (STDIO): {SERVER_SCRIPT_PATH}")

        if not os.path.exists(SERVER_SCRIPT_PATH):
            raise FileNotFoundError(f"Nie znaleziono pliku serwera: {SERVER_SCRIPT_PATH}")

        # Ważne: Przekazujemy zmienne środowiskowe do serwera (klucze API itp.)
        server_env = os.environ.copy()

        server_params = StdioServerParameters(
            command="python",
            args=[SERVER_SCRIPT_PATH],
            env=server_env
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream=read_stream, write_stream=write_stream) as session:
                print("[Client A2A] Sesja STDIO utworzona. Inicjalizacja...")
                await session.initialize()
                print("[Client A2A] Sesja STDIO gotowa.")
                yield session
    else:
        raise ValueError(f"Nieobsługiwany transport: {transport}. Wybierz 'sse' lub 'stdio'.")


# ==============================================================================
# GŁÓWNA PĘTLA CZATU
# ==============================================================================
async def run_chat_loop():
    print(f"Katalog roboczy: {os.getcwd()}")

    # Wybór transportu: 'stdio' (lokalnie) lub 'sse' (jeśli serwer działa niezależnie)
    # W architekturze A2A docelowo używa się 'sse', ale do devu lokalnego 'stdio' jest wygodniejsze.
    # selected_transport = "stdio"
    selected_transport = "sse"

    # Używamy context managera do obsługi połączenia (Nowość A2A)
    async with init_session(transport=selected_transport) as session:

        # 1. Pobranie narzędzi z serwera MCP
        try:
            mcp_tools = await session.list_tools()
            tool_names = [t.name for t in mcp_tools.tools]
            print(f"Znaleziono narzędzia na serwerze: {tool_names}")
        except Exception as e:
            print(f"Błąd pobierania narzędzi: {e}")
            return

        # 2. Konwersja narzędzi MCP na format LangChain
        langchain_tools = []

        for tool in mcp_tools.tools:
            # Wrapper musi przechwycić nazwę narzędzia i sesję
            # To pozwala LangChainowi wywołać asynchronicznie metodę call_tool w sesji MCP
            async def _tool_wrapper(query: str, tool_name=tool.name):
                print(f"\n[DEBUG A2A] Wywołuję narzędzie MCP: {tool_name} z query='{query}'")

                # Wywołanie przez sesję MCP
                result = await session.call_tool(tool_name, arguments={"query": query})

                # Obsługa błędów zwróconych przez narzędzie
                if result.isError:
                    return f"Tool Error: {result.content}"

                return result.content[0].text

            # Tworzymy StructuredTool dla LangChaina
            lc_tool = StructuredTool.from_function(
                func=None,
                coroutine=_tool_wrapper,
                name=tool.name,
                description=tool.description or "Narzędzie MCP do bazy wiedzy",
            )
            langchain_tools.append(lc_tool)

        # 3. Inicjalizacja LLM i Agenta (LangGraph)
        llm = ChatOpenAI(
            base_url=LLM_BASE_URL,
            api_key=LLM_API_KEY,
            model=LLM_MODEL,
            temperature=0
        )

        memory = MemorySaver()
        agent_executor = create_react_agent(
            llm,
            tools=langchain_tools,
            checkpointer=memory
        )

        # 4. Interaktywna pętla
        thread_id = "local-session-1"
        config = {"configurable": {"thread_id": thread_id}}

        print("=" * 50)
        print(f"ASYSTENT GOTOWY (Transport: {selected_transport}).")
        print("Zadaj pytanie o ISO20022.")
        print("=" * 50)

        while True:
            try:
                user_input = input("\nTy: ")
                if user_input.lower() in ["q", "exit", "quit"]:
                    break

                print("Asystent myśli...", end="", flush=True)

                # Przekazujemy Security Prompt w każdej iteracji
                messages_payload = [
                    SystemMessage(content=SECURITY_SYSTEM_PROMPT),
                    HumanMessage(content=user_input)
                ]

                async for event in agent_executor.astream(
                        {"messages": messages_payload},
                        config,
                        stream_mode="values"
                ):
                    last_msg = event["messages"][-1]

                    if last_msg.type == "ai":
                        if last_msg.tool_calls:
                            print(f"\n[Narzędzie] Model chce użyć: {last_msg.tool_calls[0]['name']}")
                        elif last_msg.content:
                            print(f"\r\033[K", end="")
                            print(f"\nAsystent:\n{last_msg.content}")

            except KeyboardInterrupt:
                print("\nPrzerwano.")
                break
            except Exception as e:
                print(f"\nBłąd w pętli czatu: {e}")


if __name__ == "__main__":
    asyncio.run(run_chat_loop())