from typing import List

from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation


class SignificantSentences:

    def __init__(self, text, n_sentences=4):
        self.text = text
        self.n_sentences: int = n_sentences
        self.word_ranking = dict()

    def _remove_stopwords_from_text(self) -> List[str]:
        text_lower = word_tokenize(self.text.lower())
        _stopwords = set(stopwords.words('english') + list(punctuation))

        return [word for word in text_lower if word not in _stopwords]

    def _rank_importance_of_words(self):
        word_frequency = FreqDist(self._remove_stopwords_from_text()).items()

        for i, (word, count) in enumerate(word_frequency):
            if count <= 1:
                continue
            if word not in self.word_ranking.values():
                self.word_ranking[i] = word

    def _count_important_words_in_sentence(self) -> List[tuple]:
        sentences = sent_tokenize(self.text)
        results_with_counts = []
        for sentence in sentences:
            total_word_count = 0
            for word in self.word_ranking.values():
                total_word_count += sentence.lower().count(word)
            results_with_counts.append((total_word_count, sentence))

        return sorted(results_with_counts, reverse=True)

    def get_significant_sentences(self) -> List[str]:
        self._rank_importance_of_words()
        results_with_counts = self._count_important_words_in_sentence()
        result = [pair[1] for pair in results_with_counts]
        final_result = []
        for sentence in result:
            if sentence not in final_result:
                final_result.append(sentence)

        return final_result[:self.n_sentences]
