from random import choice

import cv2
import numpy as np
from wordcloud import WordCloud

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.object_handler import ObjectHandler
from app.computer_vision.random_placement import RandomPlacement
from app.settings import Settings


class Generator:
    def __init__(self, text: str):
        self.significant_sentences = SignificantSentences(text)
        self.words = self.significant_sentences.rank_importance_of_words()
        self.object_handler = ObjectHandler(self.words)

    def make(self) -> np.array:
        self._gather_objects()

        randomizer = RandomPlacement(self._background_image(), self.object_handler.objects)
        background_base = randomizer.draw_objects()
        colormap = choice(Settings.colormaps)
        mask = cv2.bitwise_and(background_base, self._background_image())
        wordcloud = WordCloud(width=Settings.image_width,
                              height=Settings.image_height,
                              colormap=colormap,
                              max_font_size=100,
                              mask=background_base
                              ).generate(str(self.words).replace("'", ""))
        background_words = cv2.cvtColor(np.array(wordcloud), cv2.COLOR_RGB2BGR)
        return randomizer.draw_objects(background=background_words, redraw=True)

    @staticmethod
    def write_to_disk(collage_name: str, collage_image: np.array):
        cv2.imwrite(f"{Settings.collage_dir}/{collage_name}.jpg", collage_image)

    def _gather_objects(self) -> None:
        for searchword in self.words:
            self.object_handler.gather_images_from_web(searchword)
            self.object_handler.process_images_in_download_path()
            self.object_handler.cleanup_downloads()

    @staticmethod
    def _background_image() -> np.array:
        bg_img = np.zeros((Settings.image_height, Settings.image_width, 3), dtype='uint8')
        b_channel, g_channel, r_channel = cv2.split(bg_img)
        alpha_channel = np.zeros(b_channel.shape, dtype=b_channel.dtype) * 50
        return cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
