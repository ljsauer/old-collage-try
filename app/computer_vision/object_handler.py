import os
from random import randint, choice
from typing import List

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector
from app.settings import Settings
from app.web_scraper.image_search import ImageSearch


class ObjectHandler:
    def __init__(self, words: List[str]):
        self.words = words
        self.first_image = True

        self.max_images = Settings.image_per_word
        self.download_path = Settings.object_image_path
        self.objects = []

    def gather_images_from_web(self, searchword: str):
        image_searcher = ImageSearch(searchword, self.download_path, self.max_images)
        image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            image = cv2.imread(os.path.join(self.download_path, image))

            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            obj = edge_detector.obj_in_image
            if obj is not None:
                self.objects.append(obj)

    def create_text_images(self):
        for word in self.words:
            self.objects.append(self._to_image(word))

    def cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]

    @staticmethod
    def _to_image(word) -> np.array:
        word_img = np.zeros((50, 200, 4), np.uint8)
        font_face = choice([cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_ITALIC])
        cv2.putText(word_img, str(word), (15, 27), font_face,
                    1, (randint(0, 255), randint(0, 255), randint(0, 255), 255),
                    lineType=cv2.LINE_AA, bottomLeftOrigin=False)
        return word_img
