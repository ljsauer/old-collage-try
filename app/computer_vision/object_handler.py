import os
from random import randint
from typing import List

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector
from app.computer_vision.rectangle import Rectangle
from app.settings import Settings
from app.web_scraper.image_search import ImageSearch


class ObjectHandler:
    def __init__(self, words: List[str]):
        self.words = words
        self.first_image = True

        self.max_images = Settings.image_per_word
        self.download_path = Settings.object_image_path

        self.background: np.array = np.zeros(
            (Settings.image_height, Settings.image_width, 4), dtype=np.uint8
        )
        self.objects: List[np.array] = []
        self.iter_cap = 1000
        self.rectangles = []

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
                self.objects.append(obj)

    def draw_objects(self, redraw=False) -> np.array:
        if not redraw:
            self._place_objects()
        for rect, obj in zip(self.rectangles, self.objects):
            try:
                x1, y1, x2, y2 = rect.x1, rect.y1, rect.x2, rect.y2
                alpha_s = obj[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(0, 3):
                    self.background[y1:y2, x1:x2, c] = (
                            alpha_s *
                            obj[:, :, c] +
                            alpha_l *
                            self.background[y1:y2, x1:x2, c]
                    )
            except ValueError as e:
                print(e, x1, x2, y1, y2)
                continue

        return self.background

    def _place_objects(self) -> None:
        H, W = self.background.shape[:2]
        for i, obj in enumerate(self.objects):
            h, w = obj.shape[:2]
            x, y = (randint(0, W - w), randint(0, H - h))
            current = Rectangle(x, y, w, h)
            check = 0
            while self.has_collisions(current):
                current.x1 = randint(0, int(W - w))
                current.y1 = randint(0, int(H - h))
                check += 1
                if check > self.iter_cap:
                    self.objects.pop(i)
                    break
            current.x2 = int(current.x1+w)
            current.y2 = int(current.y1+h)
            self.rectangles.append(current)
        return

    def has_collisions(self, rect: Rectangle) -> bool:
        return any([rect.collides(other) for other in self.rectangles])

    def cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]
