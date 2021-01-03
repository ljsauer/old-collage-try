import os

import cv2

from app.computer_vision.edge_detector import EdgeDetector
from app.web_scraper.image_search import ImageSearch


keyword = "butterflies"
download_path = '/Users/sauerl/source/wwt/capstone/app/downloads/'

image_searcher = ImageSearch(keyword, download_path)
image_searcher.download_google_images()

for image in os.listdir(download_path):
    edge_detector = EdgeDetector(download_path+image)
    edge_detector.draw_image_as_contours()

    for obj in edge_detector.objects_in_image:
        cv2.imshow("object in image", obj)
        cv2.waitKey(0)

image_searcher.cleanup_downloads()
