import unittest

import cv2
import numpy as np

from app.computer_vision.object_handler import ObjectHandler
from app.computer_vision.rectangle import Rectangle


class TestObjectHandler(unittest.TestCase):
    def test_gather_images_from_web(self):
        mock_obj_handler = ObjectHandler(["bikes", "coffee", "earth"])
        mock_obj_handler.get_images()
        for obj in mock_obj_handler.objects:
            obj = cv2.resize(obj,
                             (int(obj.shape[1]*2), int(obj.shape[0]*2)),
                             cv2.INTER_NEAREST)
            cv2.imshow("obj", obj)
            cv2.waitKey(0)

    def test_has_collisions(self):
        rect_1 = Rectangle(0, 0, 50, 50)
        rect_2 = Rectangle(5, 5, 25, 25)
        rect_3 = Rectangle(25, 25, 25, 25)
        rect_4 = Rectangle(0, 0, 25, 25)
        rect_list = [rect_2, rect_3, rect_4]

        bg = np.ones((100, 100), dtype='uint8')
        objects = [bg]
        mock_random_placement = ObjectHandler(["pizza"])
        mock_random_placement.objects = objects
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
        mock_random_placement = ObjectHandler(["pizza"])
        mock_random_placement.objects = objects
        mock_random_placement.rectangles = rect_list
        mock_random_placement.has_collisions(rect_1)
        self.assertFalse(mock_random_placement.has_collisions(rect_1))

    def test_draw_objects(self):
        object_bg = np.ones((30, 30, 4), dtype='uint8') * 200
        img1 = object_bg.copy()
        objects = [img1] * 25
        mock_random_placement = ObjectHandler(["pizza"])
        mock_random_placement.objects = objects
        mock_random_placement.draw_objects()
        cv2.imshow("result", mock_random_placement.background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
