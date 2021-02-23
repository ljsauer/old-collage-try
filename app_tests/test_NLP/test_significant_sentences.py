import unittest

from app.NLP.significant_sentences import SignificantSentences


class TestSignificantSentences(unittest.TestCase):

    def setUp(self) -> None:
        self.text = "Banana apple pear, peach pear, pineapple peach, pear apple! Peach peach. " \
                    "Apple, peach pear. Banana pine?"
        self.sig_sents = SignificantSentences(self.text)

    def test_rank_importance_of_words(self):
        result = self.sig_sents.rank_importance_of_words()
        self.assertTrue('peach' == result[0])
        self.assertTrue('pine' == result[-1])
