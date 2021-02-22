import unittest

import cv2
import numpy as np

from app.computer_vision.rectangle import Rectangle


class TestRandomPlacement(unittest.TestCase):
    def test_has_collisions(self):
        rect_1 = Rectangle(0, 0, 50, 50)
        rect_2 = Rectangle(5, 5, 25, 25)
        rect_3 = Rectangle(25, 25, 25, 25)
        rect_4 = Rectangle(0, 0, 25, 25)
        rect_list = [rect_2, rect_3, rect_4]

        bg = np.ones((100, 100), dtype='uint8')
        objects = [bg]
        mock_random_placement = RandomPlacement(bg, objects)
        mock_random_placement.rectangles = rect_list
        mock_random_placement.has_collisions(rect_1)
        self.assertTrue(mock_random_placement.has_collisions(rect_1))

    def test_has_no_collisions(self):
        rect_1 = Rectangle(0, 0, 50, 50)
        rect_2 = Rectangle(51, 51, 19, 19)
        rect_3 = Rectangle(71, 71, 9, 9)
        rect_4 = Rectangle(85, 85, 10, 10)
        rect_list = [rect_2, rect_3, rect_4]

        bg = np.ones((100, 100), dtype='uint8')
        objects = [bg]
        mock_random_placement = RandomPlacement(bg, objects)
        mock_random_placement.rectangles = rect_list
        mock_random_placement.has_collisions(rect_1)
        self.assertFalse(mock_random_placement.has_collisions(rect_1))

    def test_draw_objects(self):
        object_bg = np.ones((30, 30, 4), dtype='uint8') * 200
        img1 = object_bg.copy()
        cv2.circle(img1, (15, 15), 10, (0, 255, 255), -1)
        img2 = object_bg.copy()
        cv2.circle(img2, (15, 15), 10, (255, 0, 0), -1)
        img3 = object_bg.copy()
        cv2.circle(img3, (15, 15), 10, (0, 255, 0), -1)
        img4 = object_bg.copy()
        cv2.circle(img4, (15, 15), 10, (0, 0, 255), -1)
        objects = [img1, img2, img3, img4] * 5
        bg = np.zeros((500, 500, 4), dtype='uint8')
        mock_random_placement = RandomPlacement(bg, objects)
        mock_random_placement.draw_objects()
        cv2.imshow("result", bg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
