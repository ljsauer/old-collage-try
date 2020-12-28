from collections import defaultdict
from heapq import nlargest
from typing import List

from nltk import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation


def _remove_stopwords_from_text(text: str) -> List[str]:
    text = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))

    return [word for word in text if word not in _stopwords]


def _rank_importance_of_words(text: str) -> (List[str], defaultdict):
    sentences = sent_tokenize(text)
    rank = defaultdict(int)
    word_frequency = FreqDist(_remove_stopwords_from_text(text))

    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in word_frequency:
                rank[i] += word_frequency[w]

    return sentences, rank


def get_significant_sentences(text: str, n_sentences=5) -> List[str]:
    sentences, rankings = _rank_importance_of_words(text)
    sentence_indices = nlargest(n_sentences, rankings, key=rankings.get)

    return [sentences[j] for j in sorted(sentence_indices)]
