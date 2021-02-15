import cv2
from flask import Flask, render_template, url_for, request, Response
from werkzeug.utils import redirect

from app.computer_vision.image_collage import CollageGenerator


app = Flask(__name__, template_folder='../templates', static_folder='../static')


class UploadError(object):
    pass


@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/collage', methods=['GET', 'POST'])
def show_image():
    return redirect(url_for('static', filename='image_collage.jpg'), code=301)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        text = str(f.read())
        return generate_collage(text)
    return Response("Please try again with a new text file", status=406)


@app.route('/generate')
def generate_collage(text, num_words=15):
    collage = CollageGenerator(text,
                               num_words=num_words,
                               img_per_word=int(75/num_words)
                               ).create_collage()
    cv2.imwrite("static/image_collage.jpg", collage)
    render_template("image.html", image_collage='static/image_collage.jpg')
    return show_image()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
