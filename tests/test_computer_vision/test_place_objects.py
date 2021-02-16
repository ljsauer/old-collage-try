# import unittest
#
# import numpy as np
#
# from app.computer_vision.place_objects import PlaceObjects
#
#
# class TestPlaceObjects(unittest.TestCase):
#     def setUp(self) -> None:
#         self.objects = [[2, 2, 50, 50] for i in range(5)]
#         self.background = np.ones((600, 600, 3), dtype='uint8')
#
#     def test_place_circles_without_overlap(self):
#         po = PlaceObjects(self.objects, self.background)
#         po.randomize_placement()
#
#         print(po.grid.grid)
import random

import cv2
import numpy as np

from app.computer_vision.place_objects import Grid, Circle

circles = []
radii = [50, 75, 25, 100, 30, 15, 5]
w, h = 1200, 1200
iter_cap = 500

grid = Grid(50, w, h)

for i in range(0, 50):
    radius = random.choice(radii)
    circle = Circle(random.randint(radius, w - radius), random.randint(radius, h - radius), radius)
    check = 0
    while grid.has_collisions(circle) and check < iter_cap:
        circle.x = int(random.randint(0, w) * (w - radius * 2) + radius)
        circle.y = int(random.randint(0, h) * (w - radius * 2) + radius)
        check += 1
    grid.circles.append(circle)
    circles.append(circle)

bg = np.zeros((w, h, 3), dtype='uint8')
draw_circles = []
for circle in circles:
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    cv2.circle(bg, (circle.x, circle.y), circle.radius, color, -1, cv2.LINE_AA)

cv2.imshow("test", bg)
cv2.waitKey(0)

