import unittest

from app.NLP.significant_sentences import SignificantSentences


class TestSignificantSentences(unittest.TestCase):

    def setUp(self) -> None:
        self.text = "This is a test text. Texas toast. Text test text, Tex, text. Goodbye, Text."
        self.sig_sents = SignificantSentences(self.text)

    def test_gets_significant_sentences(self):
        self.assertEqual(
            self.sig_sents.get_significant_sentences()[0],
            "Text test text, Tex, text."
        )
        self.assertEqual(
            self.sig_sents.get_significant_sentences()[-1],
            "Texas toast."
        )
        self.assertTrue('text' in self.sig_sents.rank_importance_of_words())
        self.assertFalse('goodbye' in self.sig_sents.rank_importance_of_words())

    def test_rank_importance_of_words(self):
        important_words = self.sig_sents.rank_importance_of_words()
        self.assertEqual("text", important_words[0])
