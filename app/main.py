import os

from flask import Flask, render_template, url_for, request, flash

from pony.orm import db_session, commit
from werkzeug.utils import redirect

from app.computer_vision.collage_generator import CollageGenerator
from app.settings import Settings
from db.models.collage import Collage

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "shh"


class UploadError(object):
    pass


@db_session
@app.route('/', methods=['GET'])
def index():
    img_size = int(Settings.image_height / 4)
    with db_session:
        try:
            collages = Collage.select(lambda c: c)
            return render_template('index.html', collages=collages, img_size=img_size)
        except FileNotFoundError:
            return render_template('index.html')


@db_session
@app.route('/collage', methods=['GET', 'POST'])
def create_collage():
    f = request.files['file']
    text = str(f.read())
    generator = CollageGenerator(text)
    with db_session:
        collage = Collage(words=generator.words)
        commit()
        collage_name = f"collage-{collage.id}"
        collage.name = collage_name
        collage.path = f"{collage_name}.jpg"

    flash("Now creating your collage")
    collage_image = generator.make()
    generator.write_to_disk(collage_name, collage_image)

    return redirect(url_for('static', filename=f"{collage_name}.jpg"))


@db_session
@app.route("/update/<collage_id>", methods=['POST'])
def rename_collage(collage_id: int):
    with db_session:
        collage = Collage[collage_id]
        collage.name = request.form['name']
        commit()

    flash("Collage updated successfully")

    return redirect(url_for('index'))


@db_session
@app.route("/delete/<collage_id>", methods=['POST'])
def delete_collage(collage_id: int):
    with db_session:
        collage = Collage[collage_id]
        collage_path = collage.path
        Collage[collage_id].delete()
        commit()

    flash("Collage deleted successfully")

    os.remove(f"{Settings.collage_dir}/{collage_path}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
