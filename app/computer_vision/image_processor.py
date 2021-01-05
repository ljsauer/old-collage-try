import os
from typing import List

import cv2

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


class ImageProcessor:
    def __init__(self, search_key, download_dir_name='downloads'):
        self.search_key = search_key
        self.download_path = os.path.abspath(os.path.relpath(f'../../app/{download_dir_name}'))
        self.objects_found: List = []
        self.image_searcher = ImageSearch(search_key, self.download_path)
        self.image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            image = cv2.imread(os.path.join(self.download_path, image))
            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            for obj in edge_detector.objects_in_image:
                self.objects_found.append(obj)

    def clean_up(self):
        self.image_searcher.cleanup_downloads()
