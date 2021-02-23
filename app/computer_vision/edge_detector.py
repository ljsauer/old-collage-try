from typing import List

import cv2
import imutils
import numpy as np


class EdgeDetector:
    def __init__(self, image: np.array):
        self.image = image

        self.object: np.array = None
        self.contour_mask: np.array = np.zeros(self.image.shape[:2], dtype='uint8')

    def locate_largest_object(self) -> None:
        # apply automatic Canny edge detection
        v = np.median(self.image)
        sigma = 0.75
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        img_edges = cv2.Canny(self.image, lower, upper)

        contours = cv2.findContours(img_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        if len(contours) > 0:
            largest_object_contours = max(contours, key=cv2.contourArea)
            cv2.drawContours(self.contour_mask, largest_object_contours, -1, (200, 200, 55), 3)
            contours_poly = cv2.approxPolyDP(largest_object_contours, 3, True)
            bounding_rect = cv2.boundingRect(contours_poly)
            self._crop_object_from_image(list(bounding_rect))

        return

    def _crop_object_from_image(self, bounding_rect: List[int]) -> None:
        x, y, w, h = bounding_rect
        if x == 0:
            bounding_rect[0] = 1
        if y == 0:
            bounding_rect[1] = 1
        bg_model = np.zeros((1, 65), dtype='float')
        fg_model = np.zeros((1, 65), dtype='float')
        image_copy = self.image.copy()
        (mask, background, foreground) = cv2.grabCut(image_copy,
                                                     self.contour_mask*0,
                                                     bounding_rect,
                                                     bg_model,
                                                     fg_model,
                                                     iterCount=1,
                                                     mode=cv2.GC_INIT_WITH_RECT)
        output_mask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
        output_mask = (output_mask * 255).astype('uint8')
        obj_img = cv2.bitwise_and(image_copy, image_copy, mask=output_mask)
        tmp = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(obj_img)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        self.object = dst[y:y+h, x:x+w, :]

        return
