import unittest

import cv2
from pony.orm import db_session

from app.computer_vision.generator import Generator
from app.settings import Settings
from app_tests.factories.collage_factory import CollageFactory


class TestGenerator(unittest.TestCase):
    def test_creates_collage(self):
        text = "The short story is a crafted form in its own right. Short stories make use of plot, " \
               "resonance, and other dynamic components as in a novel, but typically to a lesser degree. " \
               "While the short story is largely distinct from the novel or novella (short novel), " \
               "authors generally draw from a common pool of literary techniques."
        generator = Generator(text)
        collage_image = generator.make()

        with db_session:
            collage = CollageFactory(words=generator.words)
            collage_name = collage.name

        generator.write_to_disk(collage_name, collage_image)
        collage_img = cv2.imread(f"{Settings.collage_dir}/{collage_name}.jpg")
        cv2.imshow("collage", collage_img)
        cv2.waitKey(0)
