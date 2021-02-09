import cv2
from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect, secure_filename

from app.NLP.book_loader import BookLoader
from app.computer_vision.image_collage import CollageGenerator


app = Flask(__name__, template_folder='../templates', static_folder='../static')


class UploadError(object):
    pass


@app.route('/')
def hello():
    return upload_file()


@app.route('/collage', methods=['GET', 'POST'])
def show_image():
    return redirect(url_for('static', filename='image_collage.jpg'), code=301)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        text = str(f.read())
        return collage_generator(text)
    raise UploadError


@app.route('/generate')
def collage_generator(text):
    collage = CollageGenerator(text, num_words=10).create_collage()
    cv2.imwrite("static/image_collage.jpg", collage)
    render_template("image.html", image_collage='static/image_collage.jpg')
    return show_image()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
