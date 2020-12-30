import os
import unittest

from app.web_scraper.image_search import ImageSearch


class TestImageSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.keyword = "coffee+mug"
        self.max_images = 4
        self.img_search = ImageSearch(
            self.keyword,
            '/Users/sauerl/source/wwt/capstone/app/downloads',
            max_images=self.max_images
        )

    def test_downloads_google_images(self):
        self.img_search.download_google_images()
        self.assertTrue(len(
            [x for x in os.listdir(self.img_search.download_path)]
        ) == self.max_images)
        self.assertNotIn('.gif', [image for image in os.listdir(self.img_search.download_path)])

    def tearDown(self) -> None:
        self.img_search.cleanup_downloads()
