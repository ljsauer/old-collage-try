import cv2
import numpy as np

from app.NLP.book_loader import BookLoader
from app.NLP.significant_sentences import SignificantSentences
from app.computer_vision.create_wordcloud import WordcloudBackground
from app.computer_vision.image_collage import ImageCollage
from app.computer_vision.image_processor import ImageProcessor


class Tchotchkesque:
    def __init__(self, text: str, num_words: int = 30, img_per_word: int = 3):
        self.num_words = num_words
        self.sig_sentences = SignificantSentences(text)
        self.sig_sentences.rank_importance_of_words(word_count=num_words)
        self.image_processor = ImageProcessor(self.sig_sentences.important_words, img_per_word)

    def _generate_background_image(self) -> np.array:
        wc = WordcloudBackground(text=self.sig_sentences.text,
                                 max_font_size=100,
                                 max_words=250,
                                 bg_color=tuple([int(c) for c in self.image_processor.bg_color])
                                 )

        return wc.create_wordcloud()

    def _gather_objects_for_collage(self) -> None:
        for i, searchword in enumerate(self.image_processor.search_words.values()):
            print(i, searchword)

            self.image_processor.gather_images_from_web(searchword)
            self.image_processor.process_images_in_download_path()
            self.image_processor.cleanup_downloads()

    def create_collage(self) -> np.array:
        self._gather_objects_for_collage()
        image_collage = ImageCollage(objects=self.image_processor.objects_found,
                                     background_img=self._generate_background_image())
        return image_collage.make_collage()


book_loader = BookLoader()
raw_text = book_loader.load('whitman-leaves.txt')
tchotchkesque = Tchotchkesque(raw_text, num_words=10)
collage = tchotchkesque.create_collage()
cv2.imwrite("final.jpg", collage)
