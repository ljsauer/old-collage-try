from random import randint
from typing import List

import numpy as np
from PIL import Image, ImageDraw


def collides(current, other):
    if current == other:
        return False

    r1_x1, r1_y1, r1_x2, r1_y2 = current
    r2_x1, r2_y1, r2_x2, r2_y2 = other
    if r1_x1 >= r2_x2 or r2_x1 >= r1_x2:
        return False
    if r1_y1 >= r2_y2 or r2_x1 >= r1_y2:
        return False

    return True


class ImageMerge:
    def __init__(self, images: List[np.array], background: np.array):
        self.images = images
        self.background = background
        self.used_area: List[List[int, int, int]] = []

    def merge(self) -> np.array:
        pass

    def _circle_mask(self, image: np.array):
        x, y = self.random_point(*image.shape[:2])
        mask = Image.new("RGBA", max(image.shape[:2]), 0)
        ImageDraw.Draw(mask).ellipse((x, y), fill=255)

    def collision(self, current):
        if any([collides(current, other) for other in self.used_area]):
            return True

    def random_point(self, h, w) -> [int, int]:
        (x, y) = (randint(0, self.background.shape[1]),
                  randint(0, self.background.shape[0]))
        while self.collision([x, y, x+w, y+h]):
            (x, y) = (randint(0, self.background.shape[1]),
                      randint(0, self.background.shape[0]))
        self.used_area.append([x, y, x+w, y+h])
        return x, y

