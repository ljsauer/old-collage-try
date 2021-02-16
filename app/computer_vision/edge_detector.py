from typing import List

import cv2
import imutils
import numpy as np


class EdgeDetector:
    def __init__(self, image: np.array, min_object_size: float = .30):
        self.image = image
        self.min_size = min_object_size
        self.obj_in_image: np.array = None
        self.contour_mask: np.array = np.ones(self.image.shape[:2], dtype='uint8') * 255
        self.biggest_contour: np.array = None

    def draw_image_as_contours(self):
        self.draw_edges_of_objects()
        cv2.drawContours(self.contour_mask, self.biggest_contour, -1, (200, 200, 55), -1)
        try:
            contours_poly = cv2.approxPolyDP(self.biggest_contour, 3, True)
            bounding_rect = cv2.boundingRect(contours_poly)
            self._crop_object_from_image(bounding_rect)
        except cv2.error:
            pass

    def draw_edges_of_objects(self):
        try:
            img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            img_edges = cv2.Canny(img_gray, 100, 255)
        except cv2.error:
            img_edges = cv2.Canny(self.image, 100, 255)

        contours = cv2.findContours(img_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        if len(contours) > 0:
            self.biggest_contour = max(contours, key=cv2.contourArea)

    def _crop_object_from_image(self, bounding_rect: List[int]):
        background = np.zeros((1, 65), dtype='float')
        foreground = np.zeros((1, 65), dtype='float')
        _mask = np.zeros(self.image.shape[:2], dtype='uint8')
        image_copy = self.image.copy()
        try:
            (mask, background, foreground) = cv2.grabCut(image_copy,
                                                         self.contour_mask*0,
                                                         bounding_rect,
                                                         background,
                                                         foreground,
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
            self.obj_in_image = dst
        except cv2.error:
            "Trouble reading image from path"
