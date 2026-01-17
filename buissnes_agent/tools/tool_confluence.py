import os
import sys
from atlassian import Confluence
from bs4 import BeautifulSoup


def _get_confluence_client():
    """Pomocnicza funkcja do autoryzacji w Atlassian Cloud"""
    url = os.getenv("CONFLUENCE_URL")
    username = os.getenv("CONFLUENCE_USERNAME")
    token = os.getenv("CONFLUENCE_API_TOKEN")

    if not all([url, username, token]):
        return None

    return Confluence(
        url=url,
        username=username,
        password=token,  # W chmurze token API podajemy jako hasło
        cloud=True
    )


def run_confluence_search(query: str) -> str:
    """
    ### WYSZUKIWANIE W CONFLUENCE (Wewnętrzna Baza Wiedzy)

    Używa CQL (Confluence Query Language) do znalezienia stron,
    a następnie BeautifulSoup do wyczyszczenia HTML z treści.
    """
    print(f"[Confluence] Szukam: '{query}'", file=sys.stderr)

    confluence = _get_confluence_client()
    if not confluence:
        return "Błąd konfiguracji: Brak zmiennych CONFLUENCE_* w pliku .env."

    try:
        # 1. Budowanie zapytania CQL
        # title ~ "x" OR text ~ "x" -> szukaj w tytule lub w treści
        # type = "page" -> ignoruj załączniki, komentarze i blogposty
        cql = f'(title ~ "{query}" OR text ~ "{query}") AND type = "page"'

        # Pobieramy max 3 wyniki, żeby nie zaśmiecić kontekstu
        results = confluence.cql(cql, limit=3)

        if not results.get("results"):
            return "Nie znaleziono żadnych dokumentów wewnętrznych pasujących do zapytania."

        final_output = []

        # 2. Iteracja po wynikach i pobieranie treści
        for page in results["results"]:
            page_id = page["content"]["id"]
            page_title = page["content"]["title"]

            # Konstrukcja linku do strony (dla użytkownika)
            base_url = os.getenv('CONFLUENCE_URL')
            webui = page['content']['_links']['webui']
            # Czasem webui zawiera już /wiki, czasem nie - normalizacja:
            page_url = f"{base_url}/wiki{webui}" if not webui.startswith('/wiki') else f"{base_url}{webui}"

            # Pobranie pełnej treści (body.storage = format HTML Confluence'a)
            full_page = confluence.get_page_by_id(page_id, expand='body.storage')
            raw_html = full_page['body']['storage']['value']

            # 3. HTML Parsing & Cleaning
            # LLM czysty tekst niż <div><span>...
            soup = BeautifulSoup(raw_html, "html.parser")
            text_content = soup.get_text(separator="\n").strip()

            # Ograniczenie długości per strona
            max_chars = int(os.getenv("CONFLUENCE_MAX_CHARS", 2000))
            if len(text_content) > max_chars:
                text_content = text_content[:max_chars] + "\n...(ucięto resztę strony)..."

            final_output.append(f"--- STRONA CONFLUENCE: {page_title} ---\nURL: {page_url}\nTREŚĆ:\n{text_content}\n")

        return "\n".join(final_output)

    except Exception as e:
        return f"Błąd komunikacji z API Confluence: {str(e)}"