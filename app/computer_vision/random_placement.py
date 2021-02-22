from random import randint
from typing import List, Optional

import numpy as np

from app.computer_vision.rectangle import Rectangle


class RandomPlacement:
    def __init__(self, background: np.array, objects: List[np.array]):
        self.background = background
        self.objects = objects
        self.iter_cap = 1000
        self.rectangles = []

    def draw_objects(self, background: Optional[np.array] = None, redraw=False) -> np.array:
        if not redraw:
            self._place_objects()
        if background is not None:
            self.background = background
        for rect, obj in zip(self.rectangles, self.objects):
            try:
                x, y = rect.x1, rect.y1
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
            except ValueError as e:
                print(e)
                continue

        return self.background

    def _place_objects(self) -> None:
        H, W = self.background.shape[:2]
        for i, obj in enumerate(self.objects):
            h, w = obj.shape[:2]
            x, y = (randint(0, W - w), randint(0, H - h))
            current = Rectangle(x, y, w, h)
            check = 0
            while self.has_collisions(current):
                current.x1 = randint(0, int(W - w))
                current.y1 = randint(0, int(H - h))
                check += 1
                if check > self.iter_cap:
                    self.objects.pop(i)
                    return
            self.rectangles.append(current)
        return

    def has_collisions(self, rect: Rectangle) -> bool:
        return any([rect.collides(other) for other in self.rectangles])
