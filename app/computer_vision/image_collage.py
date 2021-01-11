from random import randint
from typing import List

import cv2
from shapely.geometry import Polygon, Point

import numpy as np


# TODO: Improve logic to avoid too much overlap in objects

class ImageCollage:
    def __init__(self, objects, background):
        self.objects: List[np.array] = objects
        self.background = background
        self.used_area: List[List[tuple]] = []

    def make_collage(self):
        # TODO: Rename variables to make them make sense and refactor into smaller pieces
        background_size = self.background[:2]

        for item in self.objects:
            i_y, i_x = (randint(0, background_size[0]), randint(0, background_size[1]))
            H, W = item.shape[:2]

            combos = [Polygon(area) for area in self.used_area]
            while any([Polygon(poly).contains(Point(i_x, i_y)) for poly in combos]):
                i_y, i_x = (
                    randint(0, background_size[0]),
                    randint(0, background_size[1])
                )
            while i_y + H >= background_size[0]:
                i_y -= 5
            while i_x + W >= background_size[1]:
                i_x -= 5
            while i_y <= H:
                i_y += 5
            while i_x <= W:
                i_x += 5
            self.background[i_y:i_y+H, i_x:i_x+W] = item
            self.used_area.append([(i_x, i_y),
                                   (i_x+W, i_y),
                                   (i_x+W, i_y+H),
                                   (i_x, i_y+H)])

        return self.background
