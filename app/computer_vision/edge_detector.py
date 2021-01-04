from typing import List

import cv2
import imutils
import numpy as np


class EdgeDetector:
    def __init__(self, image, min_object_size=0.75):
        self.image: np.array = image
        self.contours: List = []
        self.min_size: float = min_object_size
        self.objects_in_image: List[np.array] = []
        self.contour_mask = np.ones(self.image.shape[:2], dtype='uint8') * 255

    def draw_image_as_contours(self):
        self.draw_edges_of_objects()
        contours_poly = [None] * len(self.contours)
        boundRect = [None] * len(self.contours)
        centers = [None] * len(self.contours)
        radius = [None] * len(self.contours)
        cv2.drawContours(self.contour_mask, self.contours, -1, (200, 200, 55), -1)
        for i, c in enumerate(self.contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
        self._crop_object_from_image(boundRect)

    def draw_edges_of_objects(self):
        try:
            img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            img_edges = cv2.Canny(img_gray, 50, 100)
        except cv2.error:
            img_edges = cv2.Canny(self.image, 50, 100)

        contours = cv2.findContours(img_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = imutils.grab_contours(contours)

    def _crop_object_from_image(self, bounding_rects):
        background = np.zeros((1, 65), dtype='float')
        foreground = np.zeros((1, 65), dtype='float')
        _mask = np.zeros(self.image.shape[:2], dtype='uint8')
        image_copy = self.image.copy()
        for rectangle in bounding_rects:
            if rectangle[2]*rectangle[3] < self.min_size * self.image.shape[0] * self.image.shape[1]:
                continue
            (mask, background, foreground) = cv2.grabCut(image_copy, self.contour_mask*0, rectangle,
                                                         background, foreground, iterCount=1,
                                                         mode=cv2.GC_INIT_WITH_RECT)
            output_mask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
            output_mask = (output_mask*255).astype('uint8')
            obj_img = cv2.bitwise_and(image_copy, image_copy, mask=output_mask)
            self.objects_in_image.append(obj_img)
