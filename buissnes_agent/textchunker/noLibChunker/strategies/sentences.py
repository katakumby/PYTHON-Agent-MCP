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
        # Regex split lookbehind - dzieli po znaku interpunkcyjnym, ale go nie usuwa
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks, current = [], ""
        for sentence in sentences:
            if len(current) + len(sentence) <= self.chunk_size:
                current += " " + sentence
            else:
                chunks.append(current.strip())
                current = sentence

        if current.strip():
            chunks.append(current.strip())

        return self._apply_overlap(chunks)