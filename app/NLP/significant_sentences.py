from typing import List

from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, gutenberg
from string import punctuation


class SignificantSentences:

    def __init__(self, text: str, n_sentences: int = 4):
        try:
            self.text = gutenberg.raw(text)
        except OSError:
            self.text = text
        self.n_sentences = n_sentences
        self.important_words = dict()

    def _remove_stopwords_from_text(self) -> List[str]:
        text_lower = word_tokenize(self.text.lower())
        _stopwords = set(stopwords.words('english') + list(punctuation))

        return [word.strip("'-`") for word in text_lower
                if len(word) > 2 and word not in _stopwords]

    def rank_importance_of_words(self, word_count: int = 50) -> None:
        freq_dist = FreqDist(self._remove_stopwords_from_text()).items()
        word_frequency = sorted(freq_dist, key=lambda x: x[1], reverse=True)

        for i, (word, freq) in enumerate(word_frequency):
            if i >= word_count:
                return
            if freq <= 1:
                continue
            if word not in self.important_words.values():
                self.important_words[i] = word

    def _count_important_words_in_sentence(self) -> List[tuple]:
        sentences = sent_tokenize(self.text)
        results_with_counts = []
        for sentence in sentences:
            total_word_count = 0
            for word in self.important_words.values():
                total_word_count += sentence.lower().count(word)
            results_with_counts.append((total_word_count, sentence))

        return sorted(results_with_counts, reverse=True)

    def get_significant_sentences(self) -> List[str]:
        if len(self.important_words) == 0:
            self.rank_importance_of_words()
        results_with_counts = self._count_important_words_in_sentence()
        result = [pair[1] for pair in results_with_counts]
        final_result = []
        for i, sentence in enumerate(result):
            if i > self.n_sentences:
                return final_result
            if sentence not in final_result:
                final_result.append(sentence)
        return final_result
