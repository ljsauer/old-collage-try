import unittest

import cv2


from app.computer_vision.object_handler import ObjectHandler


class TestImageProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = ObjectHandler(["world wide web"])
        self.ip.get_images(self.ip.words[0])

    def test_processes_images(self):
        self.ip._find_objects()
        for obj in self.ip.objects:
            cv2.imshow("object", obj)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertTrue(len(self.ip.objects) != 0)

    def tearDown(self) -> None:
        self.ip._cleanup_downloads()
