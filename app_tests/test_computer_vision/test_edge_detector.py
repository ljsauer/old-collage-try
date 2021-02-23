import os
import unittest

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector


class TestEdgeDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.image = np.zeros((300, 300, 3), dtype='uint8')
        self.image = cv2.circle(self.image, (150, 150), 25, (0, 255, 255), 2)
        img = self.image.copy()
        cv2.imshow("Original", img)
        cv2.waitKey(0)
        self.ed = EdgeDetector(self.image)
        cv2.destroyAllWindows()

    def test_draws_contours(self):
        self.ed.draw_image_as_contours()
        cv2.imshow("Contours", self.ed.contour_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_finds_objects_in_image(self):
        self.ed.draw_image_as_contours()
        obj = self.ed.obj_in_image
        cv2.polylines(obj, [self.ed.biggest_contour], True, (0, 0, 255), 2, lineType=3)
        cv2.imshow("Object found", obj)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def test_crop_object_from_images():
        for image in os.listdir("test_imgs"):
            if not image.endswith(('jpg', 'png')):
                continue
            image = cv2.imread(f"test_imgs/{image}")
            ed = EdgeDetector(image)
            ed.draw_image_as_contours()
            cv2.imshow("pizza", ed.obj_in_image)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
