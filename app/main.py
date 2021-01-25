import cv2
import numpy as np

from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.create_wordcloud import WordcloudBackground
from app.computer_vision.image_collage import ImageCollage
from app.computer_vision.image_processor import ImageProcessor


class Tchotchkesque:
    def __init__(self, text_body: str, n_search_words: int = 30):
        self.significant_sents = SignificantSentences(text_body)
        self.raw_text = self.significant_sents.text
        self.n_search_words = n_search_words
        self.significant_sents.rank_importance_of_words(word_count=n_search_words)
        self.image_processor = ImageProcessor(self.significant_sents.important_words, self.n_search_words)

    def _set_collage_background(self) -> np.array:
        wc = WordcloudBackground(text=self.raw_text,
                                 mask=self.image_processor.first_image,
                                 max_font_size=100,
                                 max_words=250,
                                 bg_color=tuple([int(c) for c in self.image_processor.bg_color]))
        return wc.wordcloud

    def _gather_objects_for_collage(self) -> None:
        for i, searchword in enumerate(self.image_processor.search_words.values()):
            print(i, searchword)
            if i >= self.n_search_words:
                return
            self.image_processor.gather_images_from_web(searchword)
            self.image_processor.process_images_in_download_path()
            self.image_processor.cleanup_downloads()

    def create_collage(self) -> np.array:
        self._gather_objects_for_collage()
        image_collage = ImageCollage(objects=self.image_processor.objects_found,
                                     background_img=self._set_collage_background())
        return image_collage.make_collage()


gutenberg_book = 'whitman-leaves.txt'
tchotchkesque = Tchotchkesque(gutenberg_book, n_search_words=7)
collage = tchotchkesque.create_collage()
cv2.imwrite("final.jpg", collage)
