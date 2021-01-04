import os

import cv2

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


class ImageProcessor:
    def __init__(self, search_key, download_path='../downloads'):
        self.search_key = search_key
        self.download_path = download_path

        self.image_searcher = ImageSearch(search_key, download_path)
        self.image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            edge_detector = EdgeDetector(self.download_path+image)
            edge_detector.draw_image_as_contours()

            for obj in edge_detector.objects_in_image:
                cv2.imshow("object in image", obj)
                cv2.waitKey(0)

    def clean_up(self):
        self.image_searcher.cleanup_downloads()