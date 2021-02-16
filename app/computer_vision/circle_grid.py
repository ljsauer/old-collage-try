from random import randint
from typing import List


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.circles = []

    def adjust(self, circle: Circle) -> List:
        circle.x = int(randint(0, self.width - circle.radius))
        circle.y = int(randint(0, self.height - circle.radius))

    def add(self, circle: Circle) -> bool:
        self.circles.append(circle)

    def has_collisions(self, circle: Circle) -> bool:
        if any([collides(circle, other) for other in self.circles]):
            return True


def collides(circle: Circle, other: Circle) -> bool:
    if circle == other:
        return False
    dx = circle.x - other.x
    dy = circle.y - other.y
    rr = circle.radius + other.radius
    return (dx * dx + dy * dy) < (rr * rr)
