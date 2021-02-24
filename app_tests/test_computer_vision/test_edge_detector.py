import os
import unittest

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector


class TestEdgeDetector(unittest.TestCase):
    def test_draws_contours(self):
        self.image = np.zeros((300, 300, 3), dtype='uint8')
        self.image = cv2.circle(self.image, (150, 150), 25, (0, 255, 255), 2)
        img = self.image.copy()
        self.ed = EdgeDetector(self.image)
        self.ed.locate_largest_object()
        cv2.imshow("Draw contours", img)
        cv2.waitKey(0)
        cv2.imshow("Draw contours", self.ed.contour_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def test_crop_object_from_images():
        for image in os.listdir("test_imgs"):
            if not image.endswith(('jpg', 'png')) or image.endswith('shapes.jpg'):
                continue
            image = cv2.imread(f"test_imgs/{image}")
            cv2.imshow("Find pizza", image)
            cv2.waitKey(0)
            ed = EdgeDetector(image)
            ed.locate_largest_object()
            cv2.imshow("Find pizza", ed.object)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_locates_largest_object(self):
        image = cv2.imread("test_imgs/shapes.jpg")
        cv2.imshow("Locate largest object", image)
        cv2.waitKey(0)
        ed = EdgeDetector(image)
        ed.locate_largest_object()
        cv2.imshow("Locate largest object", ed.object)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
