import os

import cv2
import numpy as np

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.image_collage import ImageCollage
from app.computer_vision.image_processor import ImageProcessor
from app.web_scraper.image_search import ImageSearch


class Tchotchkesque:
    def __init__(self, text_body, n_search_words=30):
        self.significant_sents = SignificantSentences(text_body)
        self.n_search_words = n_search_words
        self.significant_sents.rank_importance_of_words(word_count=n_search_words)
        self.tchotchkes = []
        self.image_processor = ImageProcessor(self.significant_sents.important_words, self.n_search_words)

    def _set_collage_background(self):
        bg_keyword = self.significant_sents.important_words.get(1)
        image_searcher = ImageSearch(keyword=f'{bg_keyword} high resolution',
                                     download_path=os.path.abspath(''),
                                     max_images=5)
        image_searcher.download_background_image()
        return os.path.join(image_searcher.download_path, 'background.png')

    def _gather_objects_for_collage(self):
        for i, searchword in enumerate(self.image_processor.search_words.values()):
            print(i, searchword)
            if i > self.n_search_words:
                return
            self.image_processor.gather_images_from_web(searchword)
            self.image_processor.process_images_in_download_path()
            self.tchotchkes.append(self.image_processor.object_found)
            self.image_processor.cleanup_downloads()

    def create_collage(self) -> np.array:
        self._gather_objects_for_collage()
        image_collage = ImageCollage(objects=self.tchotchkes,
                                     background_path=self._set_collage_background())
        return image_collage.make_collage()


gutenberg_book = 'whitman-leaves.txt'
tchotchkesque = Tchotchkesque(gutenberg_book, n_search_words=40)
collage = tchotchkesque.create_collage()
cv2.imwrite("final.jpg", collage)
