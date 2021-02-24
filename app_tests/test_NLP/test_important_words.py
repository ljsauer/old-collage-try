import unittest

from app.NLP.important_words import ImportantWords


class TestSignificantSentences(unittest.TestCase):
    def test_rank_importance_of_words(self):
        self.text = "Banana apple pear, peach pear, pineapple peach, pear apple! Peach peach. " \
                    "Apple, peach pear. Banana pine?"
        self.imp_words = ImportantWords(self.text)
        result = self.imp_words.rank_by_frequency()
        self.assertTrue('peach' == result[0])
        self.assertTrue('pine' == result[-1])

    def test_cleans_words(self):
        text = "This -is. [some) text~ that! " \
               "could&use some. cleaning, up12345 " \
               "alph@betical 0rder hello-goodbye " \
               "here's some easier? text to/read " \
               "also for the, sake of being thorough"
        imp_words = ImportantWords(text)
        result = imp_words.rank_by_frequency()
        print(result)
