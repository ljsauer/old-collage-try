from math import floor, ceil
from random import randint
from typing import List

import numpy as np


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class Grid:
    def __init__(self, radius, width, height):
        grid_x = int(width / radius)
        grid_y = int(height / radius)
        self.grid = [[[] for i in range(grid_x)] for i in range(grid_y)]

        self.cell_width = int(width / grid_x)
        self.cell_height = int(height / grid_y)
        self.circles = []

    def get_cells(self, circle: Circle) -> List:
        grid_x1 = floor((circle.x - circle.radius) / self.cell_width)
        grid_x2 = ceil((circle.x + circle.radius) / self.cell_width)
        grid_y1 = floor((circle.y - circle.radius) / self.cell_height)
        grid_y2 = ceil((circle.y + circle.radius) / self.cell_height)

        cells = []
        for i in range(grid_y1, grid_y2):
            for j in range(grid_x1, grid_x2):
                cells.append(self.grid[i][j])
        return cells

    def add(self, circle: Circle) -> bool:
        self.circles.append(circle)

    def has_collisions(self, circle: Circle) -> bool:
        if any([collides(circle, other) for other in self.circles]):
            return True


class PlaceObjects:
    def __init__(self, objects: List[List], background: np.array):
        self.circles = [Circle(rect) for rect in objects]
        self.h, self.w = background.shape[:2]
        self.grid = Grid(len(self.circles), self.w, self.h)

    def randomize_placement(self):
        for i in range(0, len(self.circles)):
            while self.grid.has_collisions(self.circles[i]):
                self.circles[i].x = randint(0, self.w)
                self.circles[i].y = randint(0, self.h)
            self.grid.add(self.circles[i])


def collides(circle: Circle, other: Circle) -> bool:
    if circle == other:
        return False
    dx = circle.x - other.x
    dy = circle.y - other.y
    rr = circle.radius + other.radius
    return (dx * dx + dy * dy) < (rr * rr)
