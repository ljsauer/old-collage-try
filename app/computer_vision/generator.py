from random import choice, randint

import cv2
import numpy as np
from wordcloud import WordCloud

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.object_handler import ObjectHandler
from app.settings import Settings


class Generator:
    def __init__(self, text: str):
        self.significant_sentences = SignificantSentences(text)
        self.words = self.significant_sentences.rank_importance_of_words()
        self.object_handler = ObjectHandler(self.words)

    def make(self) -> np.array:
        self.object_handler.get_images()

        mask = self.object_handler.draw_objects()

        self.object_handler.background = self._wordcloud_background(mask)

        return self.object_handler.draw_objects(redraw=True)

    @staticmethod
    def write_to_disk(collage_name: str, collage_image: np.array):
        cv2.imwrite(f"{Settings.collage_dir}/{collage_name}.jpg", collage_image)

    def _wordcloud_background(self, mask: np.array) -> np.array:
        colormap = choice(Settings.colormaps)
        wordcloud = WordCloud(width=Settings.image_width,
                              height=Settings.image_height,
                              colormap=colormap,
                              background_color=(randint(0, 255), randint(0, 255), randint(0, 255)),
                              max_font_size=Settings.max_word_size,
                              mask=mask
                              ).generate(str(self.words).replace("'", ""))
        return cv2.cvtColor(np.array(wordcloud), cv2.COLOR_RGB2BGR)
