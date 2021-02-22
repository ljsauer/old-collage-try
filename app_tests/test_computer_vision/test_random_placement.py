from random import randint, choice

import cv2
import numpy as np

from app.computer_vision.grid import Grid, Circle

circles = []
radii = [50, 75, 25, 100, 30, 15, 10, 45, 110]
w, h = 1024, 768
iter_cap = 10000

grid = Grid(w, h)

for i in range(0, 50):
    radius = choice(radii)
    circle = Circle(randint(radius, w - radius),
                    randint(radius, h - radius),
                    radius)
    check = 0
    while grid.has_collisions(circle) and check < iter_cap:
        circle.x = int(randint(0, w) * (w - circle.radius * 2) + circle.radius)
        circle.y = int(randint(0, h) * (w - circle.radius * 2) + circle.radius)
        check += 1
    grid.add(circle)

bg = np.zeros((h, w, 3), dtype='uint8')
for circle in grid.circles:
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    cv2.circle(bg, (circle.x, circle.y), circle.radius, color, -1, cv2.LINE_AA)

cv2.imshow("test", bg)
cv2.waitKey(0)
