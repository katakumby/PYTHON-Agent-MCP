import re
from typing import List
from ..base import BaseNoLibStrategy


class MarkdownStrategy(BaseNoLibStrategy):
    """
    ### Strategia 3: Markdown Headers (Regex)

    **Jak działa:**
    Używa Regex (multiline), aby znaleźć nagłówki Markdown (#, ##, ###).
    Dzieli tekst w miejscach wystąpienia nagłówka.

    **Zastosowanie:**
    Dokumentacja techniczna, README.md. Pozwala zachować logiczną spójność sekcji.
    """

    def split_text(self, text: str) -> List[str]:
        # Dzieli tekst używając lookahead (?=...), co pozwala zachować nagłówek w następnym bloku
        blocks = re.split(r'(?=^#{1,3}\s)', text, flags=re.MULTILINE)
        blocks = [b.strip() for b in blocks if b.strip()]

        return self._apply_overlap(blocks)