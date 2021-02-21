import os
import unittest

import cv2

from app.settings import Settings
from app.web_scraper.image_search import ImageSearch


class TestImageSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.keyword = "coffee"
        self.img_search = ImageSearch(self.keyword)

    def test_downloads_google_images(self):
        self.img_search.download_google_images()
        images = [x for x in os.listdir(self.img_search.download_path)]
        for image in images[:4]:
            path = f"{Settings.object_image_path}/{image}"
            image = cv2.imread(path)
            cv2.imshow("image", image)
            cv2.waitKey(0)
        self.assertTrue(len(images) == Settings.image_per_word)
        self.assertNotIn('.gif', images)

    def tearDown(self) -> None:
        self.img_search.cleanup_downloads()
