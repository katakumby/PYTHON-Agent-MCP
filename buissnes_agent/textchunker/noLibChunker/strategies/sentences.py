import re
from typing import List
from ..base import BaseNoLibStrategy


class SentencesStrategy(BaseNoLibStrategy):
    """
    ### Strategia 2: Sentence Split (Podział na zdania)

    **Jak działa:**
    1. Używa Regex do znalezienia końców zdań (.!?).
    2. Iteruje po zdaniach i skleja je w jeden chunk, dopóki nie przekroczy `chunk_size`.
    3. Gdy limit jest osiągnięty, zamyka chunk i zaczyna nowy.
    4. Na końcu aplikuje overlap za pomocą odziedziczonej metody `_apply_overlap`.

    **Zastosowanie:**
    Zwykły tekst, artykuły, e-maile. Dużo lepsze niż `fixed` bo nie tnie słów.
    """

    def split_text(self, text: str) -> List[str]:
        # Regex split lookbehind - dzieli po znaku interpunkcyjnym
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks, current = [], ""
        for sentence in sentences:
            # Poprawka: Dodajemy +1 do długości, bo za chwilę dodamy spację
            # Jeśli current jest pusty, to nie dodajemy spacji, więc długość jest ok
            needed_space = 1 if current else 0

            if len(current) + len(sentence) + needed_space <= self.chunk_size:
                if current:
                    current += " " + sentence
                else:
                    current = sentence
            else:
                # Zapisujemy obecny chunk
                if current:
                    chunks.append(current.strip())
                # Zaczynamy nowy od bieżącego zdania
                current = sentence

        if current.strip():
            chunks.append(current.strip())

        return self._apply_overlap(chunks)