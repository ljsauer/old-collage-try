import os
from typing import Optional, List

from flask import Flask, render_template, url_for, request, flash

from pony.orm import db_session, commit
from werkzeug.utils import redirect

from app.computer_vision.generator import Generator
from app.settings import Settings
from db.models.collage import Collage

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "shh"


class UploadError(object):
    pass


@db_session
@app.route('/', methods=['GET'])
def index(collages: Optional[List[Collage]] = False):
    img_size = int(Settings.image_height / 4)
    with db_session:
        if not collages:
            collages = Collage.select(lambda c: c)
        try:
            return render_template('index.html', collages=collages, img_size=img_size)
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
        collage = Collage.select(lambda c: c.id == collage_id)
        collage.name = request.form['name']
        commit()
        collages = Collage.select(lambda c: c)

    flash("Collage Updated Successfully")

    return index(collages)


@db_session
@app.route("/delete/<collage_id>", methods=['POST'])
def delete_collage(collage_id: int):
    with db_session:
        collage = Collage.select(lambda c: c.id == collage_id)
        collage_path = collage.path
        Collage[collage_id].delete()
        commit()

    flash("Collage Deleted Successfully")

    os.remove(f"{Settings.collage_dir}/{collage_path}")

    return index()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
