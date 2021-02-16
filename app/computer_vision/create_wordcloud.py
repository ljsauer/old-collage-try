import cv2
import numpy as np
from wordcloud import WordCloud

# TODO: Create mask from randomly placed images, THEN create wordcloud


class WordcloudBackground:
    def __init__(self,
                 text: str,
                 max_font_size: int = 50,
                 max_words: int = 100,
                 bg_color: tuple[int] = None,
                 width: int = 1920,
                 height: int = 1080,
                 mask: np.array = None):
        self.text = text,
        self.max_font_size = max_font_size,
        self.max_words = max_words,
        self.bg_color = bg_color,
        self.width = width,
        self.height = height,
        self.mask = mask
        if self.mask is None:
            self._create_mask()

        self.wordcloud = WordCloud(max_font_size=max_font_size,
                                   max_words=max_words,
                                   background_color=bg_color,
                                   width=width,
                                   height=height,
                                   mask=self.mask).generate(text)

    def _create_mask(self):
        # Creates a circular mask to shape the word cloud
        if self.bg_color is None:
            self.bg_color = ([0, 0, 0])
        if self.mask is None:
            radius_size = min(self.height[0], self.width[0]) // 2
            bg = np.ones((self.height[0], self.width[0]), dtype='uint8') * 255
            self.mask = cv2.circle(bg,
                                   (self.width[0]//2, self.height[0]//2),
                                   radius_size,
                                   (0,),
                                   -1)

    def create_wordcloud(self):
        return cv2.cvtColor(np.array(self.wordcloud), cv2.COLOR_RGB2BGR)
