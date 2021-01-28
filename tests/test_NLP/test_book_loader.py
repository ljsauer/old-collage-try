import unittest

from app.NLP.book_loader import BookLoader


class TestBookLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.gutenberg_text = 'whitman-leaves.txt'
        self.raw_text = 'Once upon a time, there was a book. But this' \
                        ' is not a book. The end.'

    def test_loads_raw_text(self):
        book_loader = BookLoader()
        text = book_loader.load(self.raw_text)

        self.assertEqual(text, self.raw_text)

    def test_loads_gutenberg_text(self):
        book_loader = BookLoader()
        text = book_loader.load(self.gutenberg_text)

        self.assertNotEqual(self.gutenberg_text, text)
