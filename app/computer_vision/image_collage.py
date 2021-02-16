from typing import List

import cv2
import numpy as np

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.create_wordcloud import WordcloudBackground
from app.computer_vision.image_processor import ImageProcessor

from app.computer_vision.random_placement import RandomPlacement

# TODO: Place objects around wordcloud circle in center of background


class CollageGenerator:
    def __init__(self, text: str, num_words: int = 30, img_per_word: int = 5):
        self.num_words = num_words
        self.sig_sentences = SignificantSentences(text)
        self.sig_sentences.rank_importance_of_words(word_count=num_words)
        self.image_processor = ImageProcessor(self.sig_sentences.important_words, img_per_word)

    def _generate_background_image(self) -> np.array:
        wc = WordcloudBackground(text=str(list(self.sig_sentences.important_words.values())).replace("'", ""),
                                 max_font_size=300,
                                 bg_color=self.image_processor.bg_color
                                 )

        return wc.create_wordcloud()

    def _gather_objects_for_collage(self) -> None:
        for i, searchword in enumerate(self.image_processor.search_words.values()):
            self.image_processor.gather_images_from_web(searchword)
            self.image_processor.process_images_in_download_path()
            self.image_processor.cleanup_downloads()

    def create_collage(self) -> np.array:
        self._gather_objects_for_collage()
        image_collage = ImageCollage(objects=self.image_processor.objects_found,
                                     background_img=self._generate_background_image())
        return image_collage.make_collage()

# TODO: Refactor redundant class


class ImageCollage:
    def __init__(self, objects: List[np.array], background_img: np.array):
        self.objects = objects

        b_channel, g_channel, r_channel = cv2.split(background_img)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50
        self.background = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    def make_collage(self):
        RandomPlacement(self.background, self.objects).draw_objects()

        return self.background
