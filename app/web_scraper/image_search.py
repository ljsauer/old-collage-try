import os

import requests
from bs4 import BeautifulSoup


class ImageSearch:
    def __init__(self, keyword: str, download_path: str, max_images: int = 5):
        self.keyword = keyword.replace(' ', '+')
        self.download_path = download_path
        self.max_images = max_images

        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

    def download_google_images(self):
        url = 'https://www.google.com/search?q=' + self.keyword + \
              '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved=' \
              '0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
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
            with open(f"{self.download_path}/temp-{count}.jpg", 'wb') as f:
                f.write(img_response.content)
                f.close()
            count += 1

    def cleanup_downloads(self):
        [os.remove(self.download_path+'/'+image)
         for image in os.listdir(self.download_path)]

