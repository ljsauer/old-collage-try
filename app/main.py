import os
from typing import List

import cv2
import numpy as np

from nltk.corpus import gutenberg

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.image_collage import ImageCollage
from app.computer_vision.image_processor import ImageProcessor
from app.web_scraper.image_search import ImageSearch


class Tchotchkesque:
    def __init__(self, text_body, n_search_words: int = 20):
        self.significant_sents = SignificantSentences(text_body)
        self.significant_sents.rank_importance_of_words(word_count=n_search_words)
        self.tchotchkes = []
        self.image_processor = ImageProcessor(self.significant_sents.important_words)

    def _set_collage_background(self):
        bg_keyword = self.significant_sents.important_words.get(1)
        image_searcher = ImageSearch(keyword=f'{bg_keyword} high resolution',
                                     download_path='/Users/sauerl/source/wwt/capstone/app/background')
        image_searcher.download_background_image()
        return cv2.imread(os.path.join(image_searcher.download_path, 'background.jpg'))

    def _gather_objects_for_collage(self):
        for searchword in self.image_processor.search_words.values():
            self.image_processor.gather_images_from_web(searchword)
            self.image_processor.process_images_in_download_path()
            self.tchotchkes += self.image_processor.objects_found
            self.image_processor.cleanup_downloads()

    def create_collage(self) -> np.array:
        self._gather_objects_for_collage()
        image_collage = ImageCollage(objects=self.tchotchkes,
                                     background_path=os.path.join(
                                         '/Users/sauerl/source/wwt/capstone/app/background',
                                         'background.jpg'))
        return image_collage.make_collage()


leaves_of_grass = gutenberg.raw('whitman-leaves.txt')
tchotchkesque = Tchotchkesque(leaves_of_grass, n_search_words=5)
collage = tchotchkesque.create_collage()
cv2.imwrite("final.jpg", collage)
