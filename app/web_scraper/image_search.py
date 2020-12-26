import requests
from bs4 import BeautifulSoup


def download_google(word):
    url = 'https://www.google.com/search?q=' + word + '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    count = 0
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        print(link)
        if link.endswith('gif'):
            continue
        img_response = requests.get(link)
        with open(f"downloads/temp-{count}.jpg", 'wb') as f:
            f.write(img_response.content)
            f.close()
        count += 1
