import unittest

import cv2
import numpy as np

from app.computer_vision.image_collage import ImageCollage


class TestImageCollage(unittest.TestCase):
    def setUp(self) -> None:
        blank_img = np.zeros((75, 75, 3), dtype='uint8')
        bg_img = np.ones((300, 400, 3), dtype='uint8') * 200
        cv2.imwrite("background.png", bg_img)
        self.background = r"background.png"
        self.objects = [
            cv2.circle(blank_img.copy(), (36, 36), 15, (255, 0, 0), -1),
            cv2.circle(blank_img.copy(), (36, 36), 15, (0, 0, 255), -1),
            cv2.rectangle(blank_img.copy(), (10, 10), (65, 65), (0, 255, 0), 2),
            cv2.rectangle(blank_img.copy(), (10, 10), (65, 65), (0, 255, 255), 2),
        ]
        for i, obj_img in enumerate(self.objects):
            tmp = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
            b, g, r = cv2.split(obj_img)
            rgba = [b, g, r, alpha]
            dst = cv2.merge(rgba, 4)
            self.objects[i] = dst

    def test_creates_collage(self):
        ic = ImageCollage(objects=self.objects, background_path=self.background)
        collage = ic.make_collage()
        cv2.imshow("collage", collage)
        cv2.waitKey(0)
