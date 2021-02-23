import unittest

from app.NLP.significant_sentences import ImportantWords


class TestSignificantSentences(unittest.TestCase):

    def setUp(self) -> None:
        self.text = "Banana apple pear, peach pear, pineapple peach, pear apple! Peach peach. " \
                    "Apple, peach pear. Banana pine?"
        self.sig_sents = ImportantWords(self.text)

    def test_rank_importance_of_words(self):
        result = self.sig_sents.rank_by_frequency()
        self.assertTrue('peach' == result[0])
        self.assertTrue('pine' == result[-1])
