import unittest

import cv2


from app.computer_vision.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = ImageProcessor("world wide web")

    def test_processes_images(self):
        self.ip.process_images_in_download_path()
        for obj in self.ip.objects_found:
            cv2.imshow("object", obj)
            cv2.waitKey(0)
        self.assertTrue(len(self.ip.objects_found) != 0)

    def tearDown(self) -> None:
        self.ip.clean_up()
