import random

from app_tests.factories.pony_factory import PonyFactory
from db.models.collage import Collage


class CollageFactory(PonyFactory):
    class Meta:
        model = Collage

    name = random.choice(["one", "two", "three"])
