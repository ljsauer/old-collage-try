from random import randint
from typing import List

import cv2
from shapely.geometry import Polygon, Point

import numpy as np

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.create_wordcloud import WordcloudBackground
from app.computer_vision.image_processor import ImageProcessor

# TODO: Place objects around wordcloud circle in center of background

# TODO: Improve object-placing logic to avoid overlap in objects


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


class ImageCollage:
    def __init__(self, objects: List[np.array], background_img: np.array):
        self.objects = objects
        self.used_area: List[List[tuple]] = []

        background = background_img
        b_channel, g_channel, r_channel = cv2.split(background)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50
        self.background = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    def make_collage(self):
        background_size = self.background.shape[:2]

        for item in self.objects:
            y, x = (randint(0, background_size[0]), randint(0, background_size[1]))
            H, W = item.shape[:2]

            polygons = [Polygon(area) for area in self.used_area]
            while any([Polygon(poly).contains(Point(x, y)) for poly in polygons]):
                y, x = (randint(0, background_size[0]),
                        randint(0, background_size[1])
                        )
            while y + H >= background_size[0]:
                y -= 5
            while x + W >= background_size[1]:
                x -= 5

            alpha_s = item[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                self.background[y:y+H, x:x+W, c] = (
                        alpha_s * item[:, :, c] +
                        alpha_l * self.background[y:y+H, x:x+W, c])
            self.used_area.append([(x, y),
                                   (x+W, y),
                                   (x+W, y+H),
                                   (x, y+H)])

        return self.background
