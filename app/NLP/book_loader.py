from nltk.corpus import gutenberg


class BookLoader:
    def __init__(self):
        pass

    def load(self, text: str):
        try:
            text = gutenberg.raw(text)
        except OSError:
            pass
        return text
