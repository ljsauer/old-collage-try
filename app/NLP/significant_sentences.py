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

    def _rank_importance_of_words(self) -> (List[str]):
        sentences = sent_tokenize(self.text)
        word_frequency = FreqDist(self._remove_stopwords_from_text())

        for i, sent in enumerate(sentences):
            for w in word_tokenize(sent.lower()):
                if w in word_frequency and w not in self.word_ranking.values():
                    self.word_ranking[i] = w

        return sentences

    def get_significant_sentences(self) -> List[str]:
        sentences = self._rank_importance_of_words()
        result_with_counts = sorted(
            [
                (sentence.count(word), sentence)
                for word in self.word_ranking.values()
                for sentence in sentences
            ], reverse=True)
        result = [pair[1] for pair in result_with_counts]
        final_result = []
        for sentence in result:
            if sentence not in final_result:
                final_result.append(sentence)

        return final_result[:self.n_sentences]
