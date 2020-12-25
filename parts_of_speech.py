from typing import List

import nltk
from nltk.corpus import gutenberg


def gutenberg_list_of_adjectives(text: str) -> List[str]:
    """
    :param text: The name of a text from Project Gutenberg

    Usage:
    leaves_of_grass_adjectives = gutenberg_list_of_adjectives('whitman-leaves.txt')
    """
    adjective_tags = ['JJ', 'JJR', 'JJS']
    text_body = gutenberg.raw(text)
    parts_of_speech = nltk.pos_tag(
        nltk.tokenize.word_tokenize(str(text_body).strip(r'\').split(\'\n'))
    )
    adjectives = [a[0] for a in parts_of_speech if a[1] in adjective_tags]
    return [adj.strip(r'\\') for adj in adjectives]


print(gutenberg_list_of_adjectives('shakespeare-hamlet.txt')[:50])