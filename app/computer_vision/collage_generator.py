import os
from random import randint, choice
from typing import List

import cv2
import numpy as np
from wordcloud import WordCloud

from app.NLP.significant_sentences import ImportantWords
from app.computer_vision.edge_detector import EdgeDetector
from app.computer_vision.rectangle import Rectangle
from app.settings import Settings
from app.web_scraper.image_search import ImageSearch


class CollageGenerator:
    def __init__(self, text: str):
        self.important_words = ImportantWords(text)
        self.words = self.important_words.rank_by_frequency()

        self.max_images = Settings.image_per_word
        self.download_path = Settings.object_image_path

        self.objects: List[np.array] = []
        self.iter_cap = 1000
        self.rectangles = []
        self.background: np.array = np.zeros(
            (Settings.image_height, Settings.image_width, 4), dtype=np.uint8
        )

    def make(self) -> np.array:
        self._get_images()
        mask = self._draw_objects()
        self._wordcloud_background(mask=mask)

        return self._draw_objects(redraw=True)

    @staticmethod
    def write_to_disk(collage_name: str, collage_image: np.array):
        cv2.imwrite(f"{Settings.collage_dir}/{collage_name}.jpg", collage_image)

    def _get_images(self):
        for word in self.words:
            image_searcher = ImageSearch(word)
            image_searcher.download_google_images()
            self._find_objects()
            self._cleanup_downloads()

    def _draw_objects(self, redraw=False) -> np.array:
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
                print(e)

        return self.background

    def _has_collisions(self, rect: Rectangle) -> bool:
        return any([rect.collides(other) for other in self.rectangles])

    def _cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]

    def _find_objects(self) -> None:
        for image in os.listdir(self.download_path):
            if not image.endswith(("jpg", "png")):
                continue
            image = cv2.imread(f"{Settings.object_image_path}/{image}")

            edge_detector = EdgeDetector(image)
            edge_detector.locate_largest_object()

            obj = edge_detector.object
            if obj is not None:
                self.objects.append(obj)

        return

    def _place_objects(self) -> None:
        H, W = self.background.shape[:2]
        for i, obj in enumerate(self.objects):
            h, w = obj.shape[:2]
            x, y = (randint(0, W - w), randint(0, H - h))
            current = Rectangle(x, y, w, h)
            check = 0
            while self._has_collisions(current):
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

    def _wordcloud_background(self, mask: np.array) -> None:
        colormap = choice(Settings.colormaps)
        wordcloud = WordCloud(width=Settings.image_width,
                              height=Settings.image_height,
                              colormap=colormap,
                              background_color=(randint(0, 255), randint(0, 255), randint(0, 255)),
                              max_font_size=Settings.max_word_size,
                              mask=mask
                              ).generate(str(self.words).replace("'", ""))
        self.background = cv2.cvtColor(np.array(wordcloud), cv2.COLOR_RGB2BGR)
