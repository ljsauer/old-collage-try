import os
import urllib.request as url_req
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class ImageSearch:
    def __init__(self, keyword: str,
                 download_path: str,
                 max_images: int
                 ):
        self.keyword = keyword.replace(' ', '+')
        self.download_path = download_path
        self.max_images = max_images

        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

    def download_google_images(self):
        url = f'https://www.google.com/search?q={self.keyword}%20'\
              '&tbm=isch&hl=en&tbs=itp:lineart&sa=X&ved='\
              '0CAEQpwVqFwoTCKCt4pTPve4CFQAAAAAdAAAAABAC&biw=1344&bih=916'

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

    def download_background_image(self):
        url = f'https://pexels.com/search/{self.keyword}/'
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')
        tries = 3
        for raw_img in soup.find_all('img'):
            if tries > 3:
                return
            link = raw_img.get('src')
            if link.endswith('gif'):
                continue
            print("link", link)
            img_response = requests.get(link)
            with open(f"{self.download_path}/background.png", 'wb') as f:
                f.write(img_response.content)
                f.close()

    def cleanup_downloads(self):
        [os.remove(self.download_path+'/'+image)
         for image in os.listdir(self.download_path)]
