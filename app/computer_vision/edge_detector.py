from typing import List

import cv2
import numpy as np


class EdgeDetector:
    def __init__(self, image):
        self.image: np.array = cv2.imread(image)
        self.edges: List = []
        self.objects_in_image: List[np.array] = []
        self.mask = np.zeroes(
            self.image.shape[0],
            self.image.shape[1],
            0,
            dtype=np.uint8
        )

    def detect_object_edges(self):
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        _, image_bin = cv2.threshold(image_gray, 225, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(image_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            self.edges.append(contour)
            self.objects_in_image.append(cv2.drawContours(
                self.image,
                contour,
                -1,
                (0,),
                2
                )
            )
