from random import randint
from typing import List

from app.computer_vision.circle import Circle


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.circles = []

    def adjust(self, circle: Circle) -> List:
        circle.x = randint(0, self.width - circle.radius)
        circle.y = randint(0, self.height - circle.radius)

    def add(self, circle: Circle) -> bool:
        self.circles.append(circle)

    def has_collisions(self, circle: Circle) -> bool:
        if any([self._collides(circle, other) for other in self.circles]):
            return True

    @staticmethod
    def _collides(circle: Circle, other: Circle) -> bool:
        if circle == other:
            return False
        dx = circle.x - other.x
        dy = circle.y - other.y
        rr = circle.radius + other.radius
        return (dx * dx + dy * dy) < (rr * rr)
