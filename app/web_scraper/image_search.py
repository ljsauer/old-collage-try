import os

import requests
from bs4 import BeautifulSoup

from app.settings import Settings


class ImageSearch:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.download_path = Settings.object_image_path

    def download_google_images(self):
        # Search params:
        # - safe search
        # - transparent background
        url = f"https://www.google.com/search?as_st=y&" \
              f"tbm=isch&hl=en&as_q={self.keyword}&as_epq=&as_oq=&" \
              f"as_eq=&cr=&as_sitesearch=&safe=active"

        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')

        count = 0
        for raw_img in soup.find_all('img'):
            if count == Settings.image_per_word:
                return
            link = raw_img.get('src')
            if link.endswith('gif'):
                continue
            img_response = requests.get(link)
            with open(f"{self.download_path}/temp-{count}.png", 'wb') as f:
                f.write(img_response.content)
                f.close()
            count += 1

    def cleanup_downloads(self):
        [os.remove(f"{self.download_path}/{image}") for image in os.listdir(self.download_path)]
