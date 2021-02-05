import cv2
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect

from app.NLP.book_loader import BookLoader
from app.computer_vision.image_collage import CollageGenerator


app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/collage/', methods=['GET', 'POST'])
def show_image():
    return redirect(url_for('static', filename='image_collage.jpg'), code=301)


@app.route('/load/<text>/')
def book_loader(text):
    with open('static/book.txt', 'w') as f:
        f.write(BookLoader().load(text.strip('-')))
        f.close()
    return


@app.route('/generate/')
def collage_generator():
    with open('static/book.txt', 'r') as f:
        text = f.read().replace('-', ' ')
        collage = CollageGenerator(text, num_words=10).create_collage()
        f.close()
    cv2.imwrite("static/image_collage.jpg", collage)
    return render_template("image.html", image_collage='static/image_collage.jpg')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
