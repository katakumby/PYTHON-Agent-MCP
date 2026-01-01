import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Biblioteki MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Pobieramy katalog, w którym fizycznie znajduje się ten client_for_MCP_test.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# Definiujemy pełną ścieżkę do serwera
SERVER_SCRIPT_PATH = os.path.join(BASE_DIR, "../buissnes_agent/iso_server.py")

# Pobieranie zmiennych
LLM_BASE_URL = os.getenv("CHAT_BASE_URL")
LLM_API_KEY = os.getenv("CHAT_API_KEY")
LLM_MODEL = os.getenv("CHAT_MODEL")

# ### DEFINICJA SECURITY PROMPTU ###
SECURITY_SYSTEM_PROMPT = """
Jesteś analitykiem technicznym standardu ISO 20022.
Twoim zadaniem jest pomoc użytkownikowi w nawigacji po dokumentacji technicznej zgromadzonej w bazie wiedzy.

INSTRUKCJA POSTĘPOWANIA:

KROK 1: FILTR TEMATYCZNY
- Jeśli pytanie dotyczy: aut, pogody, gotowania, polityki itp. -> Odpowiedz: "Jestem asystentem ISO 20022. Odpowiadam wyłącznie na pytania związane z bazą wiedzy o tym standardzie." i ZAKOŃCZ.
- Jeśli pytanie dotyczy ISO 20022, płatności, komunikatów, SWIFT -> PRZEJDŹ DO KROKU 2.

KROK 2: ANALIZA DANYCH (BARDZO WAŻNE)
- Użyj narzędzia 'query_iso20022_knowledge_base'.
- Przeanalizuj zwrócone fragmenty tekstu.
- Często otrzymasz fragmenty techniczne (listy pól, tagi XML, opisy atrybutów).
- NIE OCZEKUJ definicji encyklopedycznych.

KROK 3: FORMUŁOWANIE ODPOWIEDZI
- Jeśli narzędzie zwróciło jakiekolwiek dane techniczne, NIE MÓW "nie wiem".
- Zamiast tego napisz: "Na podstawie dostępnej dokumentacji..." i opisz co widzisz w tych fragmentach.
- Przykład: Jeśli użytkownik pyta "Co to ISO", a baza zwraca pola pacs.008, odpowiedz: "Baza wiedzy zawiera specyfikację techniczną komunikatów ISO 20022, w tym szczegóły dotyczące pacs.008, takie jak [wymień pola z kontekstu]."

ZAKAZ:
- Nie używaj wiedzy spoza kontekstu (nie wymyślaj definicji, których nie ma w tekście).
- Ale BĄDŹ KREATYWNY w łączeniu znalezionych faktów w odpowiedź. Nie odrzucaj technicznych danych jako "brak informacji".
"""

async def run_chat_loop():
    print(f"Katalog roboczy: {os.getcwd()}")
    print(f"Szukam serwera tutaj: {SERVER_SCRIPT_PATH}")

    if not os.path.exists(SERVER_SCRIPT_PATH):
        print("BŁĄD KRYTYCZNY: Nadal nie widzę pliku iso_server.py!")
        return

    print(f"Podłączanie do serwera MCP...")
    print(f"Model LLM: {LLM_MODEL}")

    # 1. Konfiguracja połączenia do iso_server.py
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT_PATH],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # 2. Inicjalizacja sesji MCP
            await session.initialize()

            # 3. Pobranie narzędzi z serwera
            try:
                mcp_tools = await session.list_tools()
                tool_names = [t.name for t in mcp_tools.tools]
                print(f"Znaleziono narzędzia: {tool_names}")
            except Exception as e:
                print(f"Błąd pobierania narzędzi: {e}")
                return

            # 4. Konwersja narzędzi MCP na format LangChain
            langchain_tools = []

            for tool in mcp_tools.tools:
                # Wrapper musi przechwycić tool_name
                async def _tool_wrapper(query: str, tool_name=tool.name):
                    print(f"\n[DEBUG] Wywołuję narzędzie MCP: {tool_name} z query='{query}'")
                    result = await session.call_tool(tool_name, arguments={"query": query})
                    return result.content[0].text

                lc_tool = StructuredTool.from_function(
                    func=None,
                    coroutine=_tool_wrapper,
                    name=tool.name,
                    description=tool.description or "Brak opisu",
                )
                langchain_tools.append(lc_tool)

            # 5. Inicjalizacja Agenta
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

            # 6. Pętla Czatowania
            thread_id = "local-session-1"
            config = {"configurable": {"thread_id": thread_id}}

            print("=" * 50)
            print("ASYSTENT GOTOWY. Zadaj pytanie o ISO20022.")
            print("=" * 50)

            while True:
                try:
                    user_input = input("\nTy: ")
                    if user_input.lower() in ["q", "exit", "quit"]:
                        break

                    print("Asystent myśli...", end="", flush=True)

                    messages_payload = [
                        SystemMessage(content=SECURITY_SYSTEM_PROMPT),
                        HumanMessage(content=user_input)
                    ]

                    async for event in agent_executor.astream(
                            {"messages": messages_payload},
                            {"configurable": {"thread_id": "1"}},
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
                    print(f"\nBłąd: {e}")


if __name__ == "__main__":
    asyncio.run(run_chat_loop())

# "Do czego służy komunikat JAVA.COFFEE.001?"
#
# Wynik Pozytywny (Agent korzysta z bazy):
# "Komunikat JAVA.COFFEE.001 służy do zamawiania kawy w systemie międzybankowym i został zatwierdzony w Radomiu."