import cv2
import numpy as np
from wordcloud import WordCloud


class WordcloudBackground:
    def __init__(self, text: str,
                 max_font_size: int = 50,
                 max_words: int = 100,
                 bg_color: tuple[int] = None,
                 width: int = 1920,
                 height: int = 1080):

        if bg_color is None:
            bg_color = ([0, 0, 0])

        wordcloud = WordCloud(max_font_size=max_font_size,
                              max_words=max_words,
                              background_color=bg_color,
                              width=width,
                              height=height).generate(text)

        self.wordcloud = cv2.cvtColor(np.array(wordcloud), cv2.COLOR_RGB2BGR)
