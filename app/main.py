import os

from flask import Flask, render_template, url_for, request

from pony.orm import db_session, commit
from werkzeug.utils import redirect

from app.computer_vision.generator import Generator
from app.settings import Settings
from db.models.collage import Collage

app = Flask(__name__, template_folder='../templates', static_folder='../static')


class UploadError(object):
    pass


@app.route('/', methods=['GET'])
def index():
    img_size = int(Settings.image_height / 4)
    img_names = [name[:-4] for name in os.listdir(Settings.collage_dir)]
    try:
        return render_template('index.html',
                               images=zip(img_names, os.listdir(Settings.collage_dir)),
                               img_size=img_size)
    except FileNotFoundError:
        return render_template('index.html')


@db_session
@app.route('/collage', methods=['POST'])
def create_collage():
    f = request.files['file']
    text = str(f.read())
    generator = Generator(text)
    with db_session:
        collage = Collage(words=generator.words)
        commit()
        collage_name = f"collage-{collage.id}"

    collage_image = generator.make()
    generator.write_to_disk(collage_name, collage_image)

    return redirect(url_for('static', filename=f"{collage_name}.jpg"))


@app.route("/collage/{collage_id}")
def get_collage(collage_id: int):
    with db_session:
        collage = Collage.find(collage_id)
    return render_template("image.html", image_collage=f"/{Settings.collage_dir}_{collage.name}.jpg")


@app.route("/collage/{collage_id}", methods=['DELETE'])
def delete_collage(collage_id: int):
    with db_session:
        collage = Collage.find(collage_id)
    os.remove(f"/{Settings.collage_dir}/{collage.image_path}")
    collage.delete()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
