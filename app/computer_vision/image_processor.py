import os
from random import randint

import cv2

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


class ImageProcessor:
    def __init__(self,
                 search_words: dict[int: str],
                 max_images: int = 5,
                 download_path: str = 'downloads'
                 ):
        self.search_words = search_words
        self.first_image = True
        self.bg_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.max_images = max_images
        self.objects_found = []
        self.download_path = download_path

    def gather_images_from_web(self, searchword: str):
        image_searcher = ImageSearch(searchword, self.download_path, self.max_images)
        image_searcher.download_google_images()

    def process_images_in_download_path(self):
        for image in os.listdir(self.download_path):
            image = cv2.imread(os.path.join(self.download_path, image))

            edge_detector = EdgeDetector(image)
            edge_detector.draw_image_as_contours()

            obj = edge_detector.obj_in_image
            if obj is not None:
                # obj = cv2.resize(obj, (obj.shape[1]*2, obj.shape[0]*2), cv2.INTER_NEAREST)
                self.objects_found.append(obj)

    def cleanup_downloads(self):
        [os.remove(os.path.join(self.download_path, image))
         for image in os.listdir(self.download_path)]
