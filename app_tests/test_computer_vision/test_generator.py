import unittest

import cv2
from pony.orm import db_session

from app.computer_vision.generator import Generator
from app.settings import Settings
from app_tests.factories.collage_factory import CollageFactory


class TestGenerator(unittest.TestCase):
    def test_make_collage(self):
        text = "pizza pasta italian food delivery service"
        generator = Generator(text)
        generator.words = ["pizza", "pasta", "italian", "food", "delivery", "service"]
        collage_image = generator.make()

        with db_session:
            collage = CollageFactory(words=generator.words)
            collage_name = collage.name
        generator.write_to_disk(collage_name, collage_image)
        collage_img = cv2.imread(f"{Settings.collage_dir}/{collage_name}.jpg")
        cv2.imshow("collage", collage_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
