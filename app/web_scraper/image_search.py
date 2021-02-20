import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from google_images_search import GoogleImagesSearch
from googleapiclient.errors import HttpError

from app.settings import Settings


class ImageSearch:
    SEARCH_PARAMS = {
        "q": "",
        "num": Settings.image_per_word,
        "safe": "high",
        "fileType": "jpg|png",
        "imgSize": "LARGE" or "MEDIUM" or "XLARGE"
    }
    API_KEY = "AIzaSyCNQjfV2lC1qr8XQWPD2RACTW_0-Z6JudA"
    CX_ID = "62086768b7299d083"

    def __init__(self, keyword: str, download_path: str, max_images: int):
        self.keyword = keyword
        self.download_path = download_path
        self.max_images = max_images

        self.SEARCH_PARAMS.update({"q": keyword})

        if not os.path.exists(download_path):
            print("Making download path at: ", download_path)
            os.mkdir(download_path)

    def download_google_images(self):
        try:
            # Image Search 2.0
            gis = GoogleImagesSearch(developer_key=self.API_KEY, custom_search_cx=self.CX_ID)
            gis.search(search_params=self.SEARCH_PARAMS, path_to_dir=Settings.object_image_path)
        except HttpError:
            print(f"query limit reached -- reverting to Image Search v1.0")
            url = f'https://www.google.com/search?q={self.keyword}' \
                  f'&tbm=isch&hl=en&safe=active&%2Cisz:l&sa=X' \
                  f'&ved=0CAIQpwVqFwoTCIiQ6KKW7O4CFQAAAAAdAAAAABAC&biw=1032&bih=1707'

            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')

            count = 0
            for raw_img in soup.find_all('img'):
                if count == self.max_images:
                    return
                link = raw_img.get('src')
                if link.endswith('gif'):
                    continue
                img_response = requests.get(link)
                with open(f"{self.download_path}/temp-{count}.png", 'wb') as f:
                    f.write(img_response.content)
                    f.close()
                count += 1

    @staticmethod
    def is_valid(url: str):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def cleanup_downloads(self):
        [os.remove(f"{self.download_path}/{image}") for image in os.listdir(self.download_path)]
