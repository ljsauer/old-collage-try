from random import randint
from typing import List

import cv2
from shapely.geometry import Polygon, Point

import numpy as np


# TODO: Improve logic to avoid too much overlap in objects

class ImageCollage:
    def __init__(self, objects, background_img):
        self.objects: List[np.array] = objects

        self.background = background_img
        b_channel, g_channel, r_channel = cv2.split(self.background)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50
        self.background = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        self.used_area: List[List[tuple]] = []

    def make_collage(self):
        # TODO: Rename variables to make them make sense and refactor into smaller pieces
        background_size = self.background.shape[:2]

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
            # while i_y <= H:
            #     i_y += 5
            # while i_x <= W:
            #     i_x += 5
            alpha_s = item[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                self.background[i_y:i_y+H, i_x:i_x+W, c] = (alpha_s * item[:, :, c] +
                                          alpha_l * self.background[i_y:i_y+H, i_x:i_x+W, c])
            self.used_area.append([(i_x, i_y),
                                   (i_x+W, i_y),
                                   (i_x+W, i_y+H),
                                   (i_x, i_y+H)])

        return self.background
