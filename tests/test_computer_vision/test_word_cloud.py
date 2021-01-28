import unittest

import cv2
import numpy as np
from wordcloud import WordCloud

from app.computer_vision.create_wordcloud import WordcloudBackground


class TestWordCloud(unittest.TestCase):
    def setUp(self) -> None:
        self.text = "Prepare frosting. Cream butter until smooth " \
                    "in a large bowl with an electric mixer. " \
                    "Beat in 1 cup powdered sugar at a time, mixing" \
                    " well after each addition. Mix in vanilla extract," \
                    "peppermint extract, and salt. Add heavy cream and " \
                    "beat on medium-high speed until light and fluffy, " \
                    "3 to 5 minutes."

    def test_generate_word_cloud(self):
        self.wordcloud = WordCloud(max_font_size=40,
                                   max_words=25,
                                   background_color='white').generate(self.text)
        cv2.imshow("Word Cloud", np.array(self.wordcloud))
        cv2.waitKey(0)

    def test_creates_wordcloud_background(self):
        wc = WordcloudBackground(self.text, bg_color=tuple([0, 0, 0]), width=720)
        wc.create_wordcloud()
        wc_bgr = cv2.cvtColor(wc.create_wordcloud(), cv2.COLOR_RGB2BGR)
        cv2.imshow("Word Cloud", wc_bgr)
        cv2.waitKey(0)

    def test_use_mask_to_shape_words(self):
        mask = cv2.imread('tests/test_computer_vision/bird.png')
        wc = WordcloudBackground(self.text, mask=mask, bg_color=tuple([50, 70, 90]), width=720)
        wc_bgr = cv2.cvtColor(wc.wordcloud, cv2.COLOR_RGB2BGR)
        cv2.imshow("Word Cloud", wc_bgr)
        cv2.waitKey(0)

