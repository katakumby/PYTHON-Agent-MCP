import sys
import wikipedia


def run_wikipedia_search(query: str) -> str:
    """
    ### WYSZUKIWANIE W WIKIPEDII

    Służy do pobierania definicji encyklopedycznych.
    Działa w trybie: Szukaj -> Wybierz najlepszy -> Pobierz treść.
    """
    print(f"[Wikipedia] Szukam hasła: '{query}'", file=sys.stderr)

    # Ustawienie języka Wikipedii (można zmienić na 'pl')
    wikipedia.set_lang("en")

    try:
        # 1. Wyszukiwanie listy pasujących artykułów
        search_results = wikipedia.search(query)

        if not search_results:
            return "Nie znaleziono artykułów w Wikipedii na ten temat."

        # 2. Pobranie treści pierwszego (najbardziej trafnego) wyniku
        # auto_suggest=False wyłączamy, aby biblioteka nie zgadywała "za bardzo"
        page_title = search_results[0]
        page = wikipedia.page(page_title, auto_suggest=False)

        # 3. Przycinanie treści (Content Truncation)
        # Pobieramy tylko pierwsze 1500 znaków. LLM nie potrzebuje całego artykułu,
        # zazwyczaj wstęp (lead) wystarczy do definicji.
        summary = page.content[:1500]

        return f"--- WIKIPEDIA: {page.title} ---\n{summary}\n...(tekst przycięty ze względu na limit)..."

    except wikipedia.exceptions.DisambiguationError as e:
        # Obsługa sytuacji: "Java" -> (Wyspa, Kawa, Język programowania?)
        options = ", ".join(e.options[:5])
        return f"Hasło '{query}' jest niejednoznaczne. Czy chodziło Ci o: {options}?"

    except wikipedia.exceptions.PageError:
        return f"Strona o tytule '{query}' nie istnieje, mimo że wyszukiwarka ją zasugerowała."

    except Exception as e:
        return f"Nieoczekiwany błąd Wikipedii: {str(e)}"