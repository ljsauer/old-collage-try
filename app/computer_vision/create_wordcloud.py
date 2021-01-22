import cv2
import numpy as np
from wordcloud import WordCloud


class WordcloudBackground:
    def __init__(self, text, max_font_size=50, max_words=100, bg_color='black', width=1920, height=1080):
        wordcloud = WordCloud(max_font_size=max_font_size,
                              max_words=max_words,
                              background_color=bg_color,
                              width=width,
                              height=height).generate(text)
        self.wordcloud = cv2.cvtColor(np.array(wordcloud), cv2.COLOR_RGB2BGR)
