from random import randint
from typing import List

import numpy as np

from app.computer_vision.circle_grid import Grid, Circle


class RandomPlacement(Grid):
    def __init__(self, background: np.array, objects: List[np.array]):
        super().__init__(width=background.shape[1], height=background.shape[0])
        self.background = background
        self.objects = objects
        self.iter_cap = 600

    def _place_objects(self):
        # TODO: Optimize placement around image to minimize empty space
        for obj in self.objects:
            radius = max(obj.shape[:2])
            circle = Circle(randint(0, self.width - radius),
                            randint(0, self.height - radius),
                            radius
                            )
            check = 0
            while self.has_collisions(circle) and check < self.iter_cap:
                self.adjust(circle)
                check += 1
            self.add(circle)  # TODO: Don't place image if above check doesn't pass

    def draw_objects(self):
        self._place_objects()
        for circle, obj in zip(self.circles, self.objects):
            x, y = circle.x, circle.y
            h, w = obj.shape[:2]
            alpha_s = obj[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                self.background[y:y+h, x:x+w, c] = (
                        alpha_s *
                        obj[:, :, c] +
                        alpha_l *
                        self.background[y:y+h, x:x+w, c]
                )
