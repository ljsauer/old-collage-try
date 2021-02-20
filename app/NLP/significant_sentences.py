from typing import List

from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from app.settings import Settings


class SignificantSentences:

    def __init__(self, text: str):
        self.text = text
        self.n_sentences = Settings.n_sentences

    def rank_importance_of_words(self) -> List[str]:
        freq_dist = FreqDist(self._clean_text()).items()
        word_frequency = sorted(freq_dist, key=lambda x: x[1], reverse=True)
        important_words = []

        for i, (word, freq) in enumerate(word_frequency):
            if i >= Settings.n_words:
                return important_words
            if freq <= 1:
                continue
            if word not in important_words:
                important_words.append(word)

        return important_words

    def get_significant_sentences(self) -> List[str]:
        important_words = self.rank_importance_of_words()
        results_with_counts = self._count_important_words_in_sentence(important_words)
        result = [pair[1] for pair in results_with_counts]
        final_result = []
        for i, sentence in enumerate(result):
            if i > self.n_sentences:
                return final_result
            if sentence not in final_result:
                final_result.append(sentence)
        return final_result

    def _clean_text(self) -> List[str]:
        text_lower = word_tokenize(self.text.lower())
        _stopwords = set(stopwords.words('english') + list(punctuation))
        nums = [str(n) for n in range(0, 10)]

        words = [word.replace(r'\n', '').replace(r'\r', '') for
                 word in text_lower if word not in _stopwords]

        for word in words:
            if any([n in word for n in nums]) or len(word) < 4:
                words.remove(word)
        return words

    def _count_important_words_in_sentence(self, important_words: List[str]) -> List[tuple]:
        sentences = sent_tokenize(self.text)
        results_with_counts = []
        for sentence in sentences:
            total_word_count = 0
            for word in important_words:
                total_word_count += sentence.lower().count(word)
            results_with_counts.append((total_word_count, sentence))

        return sorted(results_with_counts, reverse=True)

