import io

from flask import Flask, render_template, url_for, request

# TODO: bootstrap loading screen?

# TODO: Back button & collage info on collage page
from pony.orm import db_session, commit, buffer
from werkzeug.utils import redirect

from app.computer_vision.image_collage import CollageGenerator
from db.models.collage import Collage

app = Flask(__name__, template_folder='../templates', static_folder='../static')


class UploadError(object):
    pass


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@db_session
@app.route('/collage', methods=['POST'])
def create_collage():
    f = request.files['file']
    text = str(f.read())
    generator = CollageGenerator(
        text,
        num_words=15,
        img_per_word=5
    )
    with db_session:
        collage = Collage(image=buffer(generator.create_collage()),
                          text=generator.sig_sentences.text)
        commit()

    # TODO: Return image from database instead of writing/reading file
    return redirect(url_for('static', filename='image_collage.jpg'))


@app.route("/collage/{collage_id}")
def update_collage(collage_id: int):
    collage = Collage.find(collage_id)
    return render_template("image.html", image_collage=collage.image)


@app.route("/collage/{collage_id}", methods=['DELETE'])
def delete_collage(collage_id: int):
    collage = Collage.find(collage_id)
    os.path.unlink(f"static/{collage.image_path}")
    collage.delete()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    startup_database()
