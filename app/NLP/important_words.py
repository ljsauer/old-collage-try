from typing import List

from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from app.settings import Settings


class ImportantWords:

    def __init__(self, text: str):
        self.text = text

    def rank_by_frequency(self) -> List[str]:
        freq_dist = FreqDist(self._clean_text()).items()
        word_frequency = sorted(freq_dist, key=lambda x: x[1], reverse=True)
        important_words = []

        for i, (word, freq) in enumerate(word_frequency):
            important_words.append(word)
            if i > Settings.n_words:
                break
        return important_words

    def _clean_text(self) -> List[str]:
        text_lower = word_tokenize(self.text.lower())
        _stopwords = [
            stopwords.words('english') +
            list(punctuation) +
            Settings.undesired_words
        ]

        return [word.strip("-/',.1234567890~") for word in
                text_lower if word not in _stopwords if
                len(word) > 3]
