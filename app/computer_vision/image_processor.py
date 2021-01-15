import os
from typing import List

import cv2

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


class ImageProcessor:
    def __init__(self,
                 search_words: dict[int: str],
                 download_path: str = 'downloads',
                 ):
        self.download_path = download_path
        self.search_words = search_words
        self.objects_found: List = []

    def gather_images_from_web(self, searchword):
        image_searcher = ImageSearch(searchword, self.download_path)
        image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            image = cv2.imread(os.path.join(self.download_path, image))
            cv2.imshow("img", image)
            cv2.waitKey(0)
            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            for obj in edge_detector.objects_in_image:
                self.objects_found.append(obj)

    def cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]
