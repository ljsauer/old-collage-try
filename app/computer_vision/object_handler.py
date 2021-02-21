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

    @staticmethod
    def gather_images_from_web(searchword: str):
        image_searcher = ImageSearch(searchword)
        image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            if not image.endswith(("jpg", "png")):
                continue
            image = cv2.imread(f"{Settings.object_image_path}/{image}")

            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            obj = edge_detector.obj_in_image
            if obj is not None:
                if (
                        obj.shape[0] >= int(Settings.image_height * 0.12) or
                        obj.shape[1] >= int(Settings.image_width * 0.12)
                ):
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
        font_face = choice([cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_DUPLEX])
        cv2.putText(word_img, str(word), (15, 27), font_face,
                    1, (randint(0, 255), randint(0, 255), randint(0, 255), 255),
                    lineType=cv2.LINE_AA, bottomLeftOrigin=False)
        return word_img
