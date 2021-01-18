import os
from typing import List

import cv2
import numpy as np

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


class ImageProcessor:
    def __init__(self,
                 search_words: dict[int: str],
                 max_images: int = 5,
                 download_path: str = 'downloads'
                 ):
        self.search_words = search_words
        self.max_images = max_images
        self.object_found: np.array = None
        self.download_path = download_path

    def gather_images_from_web(self, searchword):
        image_searcher = ImageSearch(searchword, self.download_path, self.max_images)
        image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            image = cv2.imread(os.path.join(self.download_path, image))
            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            obj = edge_detector.obj_in_image
            if obj is not None:
                obj = cv2.resize(obj, (obj.shape[1]*4, obj.shape[0]*4), cv2.INTER_NEAREST)
                self.object_found = obj

    def cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]
