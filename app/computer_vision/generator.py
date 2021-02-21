from random import randint

import cv2
import numpy as np

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
        self.object_handler.create_text_images()

        randomizer = RandomPlacement(self._background_image(), self.object_handler.objects)
        return randomizer.draw_objects()

    @staticmethod
    def write_to_disk(collage_name: str, collage_image: np.array):
        cv2.imwrite(f"{Settings.collage_dir}/{collage_name}.jpg", collage_image)

    def _gather_objects(self) -> None:
        for searchword in self.words:
            self.object_handler.gather_images_from_web(searchword)
            self.object_handler.process_images_in_download_path()
            self.object_handler.cleanup_downloads()

    @staticmethod
    def _background_image():
        bg_img = np.ones((Settings.image_height, Settings.image_width, 3), dtype='uint8')
        b_channel, g_channel, r_channel = cv2.split(bg_img)
        b_channel = b_channel * randint(0, 255)
        g_channel = g_channel * randint(0, 255)
        r_channel = r_channel * randint(0, 255)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50
        return cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
