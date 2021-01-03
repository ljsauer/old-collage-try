from typing import List

import cv2
import imutils
import numpy as np


class EdgeDetector:
    def __init__(self, image):
        self.image: np.array = cv2.imread(image)
        self.contours: List = []
        self.objects_in_image: List[np.array] = []
        self.mask = np.ones(self.image.shape[:2], dtype='uint8') * 255

    def draw_image_as_contours(self):
        self.detect_object_outlines()
        contours_poly = [None] * len(self.contours)
        boundRect = [None] * len(self.contours)
        centers = [None] * len(self.contours)
        radius = [None] * len(self.contours)
        for i, c in enumerate(self.contours):
            cv2.drawContours(self.mask, [c], -1, 0, -1)
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
        self._crop_object_from_image(boundRect)

        cv2.imshow("mask", self.mask)
        cv2.waitKey(0)

    def detect_object_outlines(self):
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        img_edges = cv2.Canny(img_gray, 50, 100)

        contours = cv2.findContours(img_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = imutils.grab_contours(contours)

    def _crop_object_from_image(self, bounding_rects):
        background = np.zeros((1, 65), dtype='float')
        foreground = np.zeros((1, 65), dtype='float')
        _mask = np.zeros(self.image.shape[:2], dtype='uint8')
        image_copy = self.image.copy()
        for rectangle in bounding_rects:
            if rectangle[2]*rectangle[3] < 0.45 * self.image.shape[0] * self.image.shape[1]:
                continue
            (mask, background, foreground) = cv2.grabCut(image_copy, self.mask*0, rectangle,
                                                         background, foreground, iterCount=1,
                                                         mode=cv2.GC_INIT_WITH_RECT)
            output_mask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
            output_mask = (output_mask*255).astype('uint8')
            obj_img = cv2.bitwise_and(image_copy, image_copy, mask=output_mask)
            self.objects_in_image.append(obj_img)
