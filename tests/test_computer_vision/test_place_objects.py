import unittest

import cv2
import numpy as np

from app.computer_vision.place_objects import PlaceObjects


class TestPlaceObjects(unittest.TestCase):
    def setUp(self) -> None:
        self.objects = [[2, 2, 50, 50] for i in range(0, 10)]
        self.background = np.ones((600, 600, 3), dtype='uint8')

    def test_place_circles_without_overlap(self):
        po = PlaceObjects(self.objects, self.background)
        po.randomize_placement()

        cv2.imshow("grid", np.array(po.grid))
        cv2.waitKey(0)

