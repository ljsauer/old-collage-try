import unittest

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector


class TestEdgeDetector(unittest.TestCase):
    def setUp(self) -> None:
        # create gray image
        self.image = np.ones((300, 300, 3), dtype='uint8') * 200
        # draw yellow circle on image
        self.image = cv2.circle(self.image, (150, 150), 25, (0, 255, 255), 2)
        img = self.image.copy()
        cv2.imshow("Original", img)
        cv2.waitKey(0)
        self.ed = EdgeDetector(self.image, min_object_size=1)

    def test_draws_contours(self):
        self.ed.draw_image_as_contours()
        cv2.imshow("Contours", self.ed.contour_mask)
        cv2.waitKey(0)

    def test_finds_objects_in_image(self):
        self.ed.draw_image_as_contours()
        for obj in self.ed.objects_in_image:
            obj = cv2.rectangle(obj,
                                (10, 10),
                                (25, 25),
                                (0, 255, 0),
                                2
                                )
            cv2.imshow("Object found", obj)
            cv2.waitKey(0)
