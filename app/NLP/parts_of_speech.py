from typing import List

import nltk
from nltk.corpus import gutenberg


class PartsOfSpeech:

    def __init__(self, text: str):
        """
        :param text: The name of a .txt file from Project Gutenberg
        """
        self.text = text

    def _process_parts_of_speech(self) -> List[tuple]:
        raw_text = gutenberg.raw(self.text)
        parts_of_speech = nltk.pos_tag(
            nltk.tokenize.word_tokenize(str(raw_text).strip(r'\').split(\'\n'))
        )
        return parts_of_speech

    def gutenberg_list_of_adjectives(self) -> List[str]:
        """
        Usage:
        leaves_of_grass_adjectives = gutenberg_list_of_adjectives('whitman-leaves.txt')
        """
        adjective_tags = ['JJ', 'JJR', 'JJS']
        pos_tags = self._process_parts_of_speech()
        adjectives = [w[0] for w in pos_tags if w[1] in adjective_tags]
        return [adj.strip(r'\\') for adj in adjectives]

    def gutenberg_list_of_verbs(self) -> List[str]:
        """
        Usage:
        leaves_of_grass_verbs = gutenberg_list_of_verbs('whitman-leaves.txt')
        """
        verb_tags = ['VN', 'VBN', 'VBD', 'VBG', 'VBP', 'VBZ']
        pos_tags = self._process_parts_of_speech()
        verbs = [w[0] for w in pos_tags if w[1] in verb_tags]
        return [v.strip(r'\\') for v in verbs]

# TODO: Create Gutenberg class to super init from PartsOfSpeech
