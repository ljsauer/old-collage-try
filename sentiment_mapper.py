from typing import List

import numpy as np


class TextAnalyzer(object):
    """

    """
    def __init__(self, text_body):
        self.text_body = text_body

    def analyze_chapters(self) -> dict:
        pass


class SentimentMapper:
    """

    """
    def __init__(self, text_body):
        self.text_body: str = text_body
        self.chapter_sentiments: dict = TextAnalyzer(text_body).analyze_chapters()
        self.image_rules: dict = dict()
